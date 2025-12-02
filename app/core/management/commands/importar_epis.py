import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from app.epi.models import EPI


class Command(BaseCommand):
    help = "Importa EPIs a partir de CSV. Faz upsert por CA (se existir) ou Nome."

    def add_arguments(self, parser):
        parser.add_argument(
            "--arquivo",
            type=str,
            required=True,
            help="Caminho do CSV (UTF-8). Cabeçalho esperado: Nome, CA, Validade CA, Categoria, Tamanho, Ativo",
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
            raise CommandError(f"Arquivo não encontrado: {caminho}")

        criados = 0
        atualizados = 0

        with caminho.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise CommandError("CSV sem cabeçalho ou vazio.")

            for row in reader:
                nome = (row.get("Nome") or "").strip()
                ca = (row.get("CA") or "").strip()
                validade_ca = self._parse_date((row.get("Validade CA") or row.get("Validade") or "").strip())
                categoria = (row.get("Categoria") or "").strip()
                tamanho = (row.get("Tamanho") or "").strip()
                ativo_raw = (row.get("Ativo") or "True").strip().lower()
                ativo = ativo_raw not in {"false", "0", "nao", "não", "n"}

                if not nome and not ca:
                    self.stdout.write(self.style.WARNING(f"Pulando linha sem Nome/CA: {row}"))
                    continue

                lookup = {"ca": ca} if ca else {"nome": nome}
                epi, created = EPI.objects.update_or_create(
                    **lookup,
                    defaults={
                        "nome": nome or f"EPI CA {ca}",
                        "ca": ca,
                        "validade_ca": validade_ca,
                        "categoria": categoria,
                        "tamanho": tamanho,
                        "ativo": ativo,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída. Criados: {criados}, Atualizados: {atualizados}"))
