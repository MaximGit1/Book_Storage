from .models import MarkDownReview
from django import forms


class CreateMarkDownReviewForm(forms.ModelForm):
    class Meta:
        model = MarkDownReview
        fields = ("body",)
