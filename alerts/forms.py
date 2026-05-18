from django import forms
from .models import Alert, Recommendation


class AlertForm(forms.ModelForm):

    class Meta:
        model = Alert

        # 👇 SOLO CAMPOS EDITABLES
        fields = [
            "tipo",
            "nivel",
            "descripcion",
        ]

        widgets = {
            "tipo": forms.Select(attrs={
                "class": "form-select"
            }),

            "nivel": forms.Select(attrs={
                "class": "form-select"
            }),

            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe la alerta..."
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tipo"].label = "Tipo de alerta"
        self.fields["nivel"].label = "Nivel de gravedad"
        self.fields["descripcion"].label = "Descripción"

        self.order_fields([
            "tipo",
            "nivel",
            "descripcion"
        ])

class RecommendationForm(forms.ModelForm):

    class Meta:
        model = Recommendation
        fields = ["titulo", "descripcion", "prioridad", "estado"]

        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "prioridad": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }
