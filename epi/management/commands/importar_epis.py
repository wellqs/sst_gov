import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from epi.models import EPI


class Command(BaseCommand):
    help = "Importa EPIs a partir de um arquivo CSV. Atualiza por CA se existir."

    def add_arguments(self, parser):
        parser.add_argument(
            "--arquivo",
            type=str,
            required=True,
            help="Caminho do CSV (UTF-8). Cabeçalho esperado: Nome,CA,Validade CA,Categoria,Tamanho,Observacoes,Ativo",
        )

    def handle(self, *args, **options):
        caminho = Path(options["arquivo"])
        if not caminho.exists():
            raise CommandError(f"Arquivo não encontrado: {caminho}")

        criados = 0
        atualizados = 0
        with caminho.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            required_headers = {"Nome", "CA"}
            missing = required_headers - set(reader.fieldnames or [])
            if missing:
                raise CommandError(f"Colunas obrigatórias ausentes: {', '.join(missing)}")

            for row in reader:
                nome = (row.get("Nome") or "").strip()
                ca = (row.get("CA") or "").strip()
                if not nome or not ca:
                    self.stdout.write(self.style.WARNING(f"Pulando linha sem Nome ou CA: {row}"))
                    continue

                validade_raw = (row.get("Validade CA") or "").strip()
                validade_ca = None
                if validade_raw:
                    try:
                        validade_ca = datetime.fromisoformat(validade_raw).date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"Data inválida para CA {ca}: {validade_raw}"))

                categoria = (row.get("Categoria") or "").strip()
                tamanho = (row.get("Tamanho") or "").strip()
                observacoes = (row.get("Observacoes") or row.get("Observações") or "").strip()
                ativo_raw = (row.get("Ativo") or "True").strip().lower()
                ativo = ativo_raw not in {"false", "0", "nao", "não", "n"}

                epi, created = EPI.objects.update_or_create(
                    ca=ca,
                    defaults={
                        "nome": nome,
                        "validade_ca": validade_ca,
                        "categoria": categoria,
                        "tamanho": tamanho,
                        "observacoes": observacoes,
                        "ativo": ativo,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída. Criados: {criados}, Atualizados: {atualizados}"))
