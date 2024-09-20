from django import forms
from .models import MarkDownReview

class CreateMarkDownReviewForm(forms.ModelForm):
    class Meta:
        model = MarkDownReview
        fields = ('body',)
