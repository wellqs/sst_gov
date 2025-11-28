from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command


class Command(BaseCommand):
    help = "Carrega dados de exemplo do diretório data/ (cargos, setores, EPIs, servidores)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            type=str,
            default=None,
            help="Diretório base onde ficam os CSVs. Padrão: <BASE_DIR>/data",
        )

    def handle(self, *args, **options):
        base_dir = Path(options["data_dir"]) if options["data_dir"] else Path(settings.BASE_DIR) / "data"
        if not base_dir.exists():
            raise CommandError(f"Diretório não encontrado: {base_dir}")

        steps = [
            ("importar_cargos", base_dir / "cargos_hospital.csv"),
            ("importar_setores", base_dir / "setores.csv"),
            ("importar_epis", base_dir / "epis.csv"),
            ("importar_servidores", base_dir / "servidores_ht.csv"),
        ]

        for cmd, path in steps:
            if not path.exists():
                self.stdout.write(self.style.WARNING(f"Pulando {cmd}: arquivo não encontrado ({path})"))
                continue
            self.stdout.write(f"Executando {cmd} com {path}")
            call_command(cmd, arquivo=str(path))

        self.stdout.write(self.style.SUCCESS("Carga de dados concluída."))
