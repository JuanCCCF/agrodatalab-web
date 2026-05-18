from django import forms
from .models import EnviroProRecord

class EnviroProRecordForm(forms.ModelForm):

    class Meta:
        model = EnviroProRecord
        fields = "__all__"

        widgets = {
            "fecha": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "humedad_media": forms.NumberInput(attrs={"class": "form-control"}),
            "temp_suelo": forms.NumberInput(attrs={"class": "form-control"}),
            "temp_max": forms.NumberInput(attrs={"class": "form-control"}),
            "temp_min": forms.NumberInput(attrs={"class": "form-control"}),
            "bateria": forms.NumberInput(attrs={"class": "form-control"}),
            "panel_solar": forms.NumberInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }
    
    # 👇 CLAVE IMPORTANTE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 ESTA ES LA CLAVE
        if self.instance and self.instance.pk and self.instance.fecha:
            self.initial["fecha"] = self.instance.fecha.strftime("%Y-%m-%dT%H:%M")