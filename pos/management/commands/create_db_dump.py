from django.core.management.base import BaseCommand
from django.conf import settings
import os
import subprocess
import datetime
from pathlib import Path


class Command(BaseCommand):
    help = 'Create a complete database dump'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path (optional)',
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['sql', 'custom', 'directory', 'tar'],
            default='sql',
            help='Output format (default: sql)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Creating database dump...')
        )

        # Get database configuration
        db_config = settings.DATABASES['default']
        
        # Create dump filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if options['output']:
            dump_path = Path(options['output'])
        else:
            dump_filename = f"akti_invoicer_dump_{timestamp}.{options['format']}"
            dump_path = Path(settings.BASE_DIR) / "database_dumps" / dump_filename
        
        # Create database_dumps directory
        dump_path.parent.mkdir(exist_ok=True)
        
        # Build pg_dump command
        cmd = [
            'pg_dump',
            '--host', db_config['HOST'],
            '--port', db_config['PORT'],
            '--username', db_config['USER'],
            '--dbname', db_config['NAME'],
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges',
        ]
        
        # Add format-specific options
        if options['format'] == 'custom':
            cmd.extend(['--format', 'custom'])
        elif options['format'] == 'directory':
            cmd.extend(['--format', 'directory'])
        elif options['format'] == 'tar':
            cmd.extend(['--format', 'tar'])
        
        cmd.extend(['--file', str(dump_path)])
        
        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['PASSWORD']
        
        self.stdout.write(f"Database: {db_config['NAME']}")
        self.stdout.write(f"Host: {db_config['HOST']}")
        self.stdout.write(f"User: {db_config['USER']}")
        self.stdout.write(f"Output: {dump_path}")
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Database dump created successfully!')
            )
            self.stdout.write(f'📁 Dump file location: {dump_path}')
            
            # Show file size
            if dump_path.exists():
                size_mb = dump_path.stat().st_size / (1024*1024)
                self.stdout.write(f'📊 File size: {size_mb:.2f} MB')
                
        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR('❌ Error creating database dump:')
            )
            self.stdout.write(f'Error: {e}')
            self.stdout.write(f'STDERR: {e.stderr}')
            return
        
        # Create Django fixtures dump
        self.stdout.write('\n📦 Creating Django fixtures dump...')
        fixtures_dir = Path(settings.BASE_DIR) / "database_dumps" / "fixtures"
        fixtures_dir.mkdir(exist_ok=True)
        
        from django.apps import apps
        app_names = [app.name for app in apps.get_app_configs() if not app.name.startswith('django.')]
        
        for app_name in app_names:
            try:
                fixture_filename = f"{app_name}_{timestamp}.json"
                fixture_path = fixtures_dir / fixture_filename
                
                fixture_cmd = [
                    'python', 'manage.py', 'dumpdata', app_name,
                    '--indent', '2',
                    '--output', str(fixture_path)
                ]
                
                subprocess.run(fixture_cmd, capture_output=True, text=True, check=True)
                self.stdout.write(f'✅ Created fixture: {fixture_filename}')
                
            except subprocess.CalledProcessError as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Warning: Could not create fixture for {app_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Database dump process completed!')
        )
        self.stdout.write(f'📁 PostgreSQL dump: {dump_path}')
        self.stdout.write(f'📁 Django fixtures: {fixtures_dir}')
        
        # Show restore instructions
        self.stdout.write('\n📋 To restore the database:')
        self.stdout.write(f'psql -h {db_config["HOST"]} -U {db_config["USER"]} -d {db_config["NAME"]} < {dump_path}')
