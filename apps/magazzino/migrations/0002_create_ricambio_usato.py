# Generated migration to add RicambioUsato model
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazzino', '0001_initial'),
        ('officina', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RicambioUsato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantita', models.PositiveIntegerField(default=1)),
                ('prezzo_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('ricambio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usi', to='magazzino.ricambio')),
                ('intervento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ricambi_usati', to='officina.intervento')),
                ('ordine_lavoro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ricambi_usati', to='officina.ordinelavoro')),
                ('movimento', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ricambio_collegato', to='magazzino.movimentomagazzino')),
            ],
        ),
    ]
