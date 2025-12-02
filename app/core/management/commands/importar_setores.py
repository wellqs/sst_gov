import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from app.core.models import Setor, Unidade


class Command(BaseCommand):
    help = "Importa setores a partir de CSV. Faz upsert por (Unidade, Nome)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--arquivo",
            type=str,
            required=True,
            help="Caminho do CSV (UTF-8). Cabeçalho: Unidade, Nome, Codigo, Descricao, Ativa",
        )

    def handle(self, *args, **options):
        caminho = Path(options["arquivo"])
        if not caminho.exists():
            raise CommandError(f"Arquivo não encontrado: {caminho}")

        criados = 0
        atualizados = 0

        with caminho.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("CSV sem cabeçalho ou vazio.")

            for row in reader:
                unidade_nome = (row.get("Unidade") or "").strip()
                nome = (row.get("Nome") or "").strip()
                if not unidade_nome or not nome:
                    self.stdout.write(self.style.WARNING(f"Pulando linha sem Unidade/Nome: {row}"))
                    continue

                codigo = (row.get("Codigo") or row.get("Código") or "").strip()
                descricao = (row.get("Descricao") or row.get("Descrição") or "").strip()
                ativa_raw = (row.get("Ativa") or "True").strip().lower()
                ativa = ativa_raw not in {"false", "0", "nao", "não", "n"}

                unidade, _ = Unidade.objects.get_or_create(nome=unidade_nome, defaults={"sigla": unidade_nome[:10]})
                setor, created = Setor.objects.update_or_create(
                    unidade=unidade,
                    nome=nome,
                    defaults={
                        "codigo": codigo,
                        "descricao": descricao,
                        "ativa": ativa,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída. Criados: {criados}, Atualizados: {atualizados}"))
