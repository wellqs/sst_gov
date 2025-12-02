import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from app.core.models import Cargo, Servidor, Setor, Unidade


class Command(BaseCommand):
    help = "Importa servidores a partir de CSV. Faz upsert por matricula (ou CPF se a matricula nao vier)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--arquivo",
            type=str,
            required=True,
            help=(
                "Caminho do CSV UTF-8. Cabecalho esperado: "
                "Nome,CPF,Matricula,Unidade,Setor,Cargo,Email,Telefone,Celular,DataNascimento,Admissao,Demissao,Ativo"
            ),
        )

    def _parse_date(self, value: str):
        if not value:
            return None
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            return None

    def handle(self, *args, **options):
        caminho = Path(options["arquivo"])
        if not caminho.exists():
            raise CommandError(f"Arquivo nao encontrado: {caminho}")

        criados = 0
        atualizados = 0
        with caminho.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("CSV sem cabecalho ou vazio.")

            for row in reader:
                nome = (row.get("Nome") or "").strip()
                cpf = (row.get("CPF") or "").strip()
                matricula = (row.get("Matricula") or "").strip()
                unidade_nome = (row.get("Unidade") or "").strip()
                setor_nome = (row.get("Setor") or "").strip()
                cargo_nome = (row.get("Cargo") or "").strip()

                if not nome or (not matricula and not cpf):
                    self.stdout.write(self.style.WARNING(f"Pulando linha sem Nome/Matricula/CPF: {row}"))
                    continue

                if not unidade_nome or not setor_nome or not cargo_nome:
                    self.stdout.write(self.style.WARNING(f"Pulando linha sem Unidade/Setor/Cargo: {row}"))
                    continue

                email = (row.get("Email") or "").strip()
                telefone = (row.get("Telefone") or "").strip()
                celular = (row.get("Celular") or "").strip()
                data_nascimento = self._parse_date((row.get("DataNascimento") or "").strip())
                admissao = self._parse_date((row.get("Admissao") or "").strip())
                demissao = self._parse_date((row.get("Demissao") or "").strip())
                ativo_raw = (row.get("Ativo") or "True").strip().lower()
                ativo = ativo_raw not in {"false", "0", "nao", "não", "n"}

                unidade, _ = Unidade.objects.get_or_create(
                    nome=unidade_nome,
                    defaults={"sigla": unidade_nome[:10]},
                )
                setor, _ = Setor.objects.get_or_create(
                    unidade=unidade,
                    nome=setor_nome,
                    defaults={"codigo": "", "descricao": "", "ativa": True},
                )
                cargo, _ = Cargo.objects.get_or_create(
                    titulo=cargo_nome,
                    defaults={"cbo": "", "descricao": "", "ativo": True},
                )

                lookup = {"matricula": matricula} if matricula else {"cpf": cpf}
                servidor, created = Servidor.objects.update_or_create(
                    **lookup,
                    defaults={
                        "nome": nome,
                        "cpf": cpf,
                        "matricula": matricula or cpf,
                        "email": email,
                        "telefone": telefone,
                        "celular": celular,
                        "data_nascimento": data_nascimento,
                        "unidade": unidade,
                        "setor": setor,
                        "cargo": cargo,
                        "admissao": admissao,
                        "demissao": demissao,
                        "ativo": ativo,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1

        self.stdout.write(self.style.SUCCESS(f"Importacao concluida. Criados: {criados}, Atualizados: {atualizados}"))
