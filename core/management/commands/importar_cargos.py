import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core.models import Cargo


class Command(BaseCommand):
    help = "Importa cargos a partir de CSV. Faz upsert por CBO (se existir) ou por título."

    def add_arguments(self, parser):
        parser.add_argument(
            "--arquivo",
            type=str,
            required=True,
            help="Caminho do CSV (UTF-8). Cabeçalho esperado: Titulo/Nome, CBO, Descricao/Descrição, Ativo",
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
                titulo = (row.get("Titulo") or row.get("Nome") or "").strip()
                cbo = (row.get("CBO") or "").strip()
                descricao = (row.get("Descricao") or row.get("Descrição") or "").strip()
                ativo_raw = (row.get("Ativo") or "True").strip().lower()
                ativo = ativo_raw not in {"false", "0", "nao", "não", "n"}

                if not titulo and not cbo:
                    self.stdout.write(self.style.WARNING(f"Pulando linha sem título/CBO: {row}"))
                    continue

                lookup = {"cbo": cbo} if cbo else {"titulo": titulo}
                cargo, created = Cargo.objects.update_or_create(
                    **lookup,
                    defaults={
                        "titulo": titulo or cbo,
                        "cbo": cbo,
                        "descricao": descricao,
                        "ativo": ativo,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída. Criados: {criados}, Atualizados: {atualizados}"))
