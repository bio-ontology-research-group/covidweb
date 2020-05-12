from django import forms
from uploader.utils import FORM_ITEMS
from uploader.models import Upload
from uploader.qc_metadata import qc_metadata
from django.forms import ValidationError
from uploader.tasks import upload_to_arvados


def add_clean_field(cls, field_name):
    def required_field(self):
        metadata_file = self.cleaned_data['metadata_file']
        value = self.cleaned_data[field_name]
        if metadata_file is not None:
            return value
        raise ValidationError("This field is required!")
    required_field.__doc__ = "Required field validator for %s" % field_name
    required_field.__name__ = "clean_%s" % field_name
    setattr(cls, required_field.__name__, required_field)

class UploadForm(forms.ModelForm):
    sequence_file = forms.FileField(
        required=True,
        help_text='Sequence file in FASTA/FASTQ format. Max file size is 512Mb.')
    metadata_file = forms.FileField(
        required=False,
        help_text='Metadata file in JSON/YAML format. Metadata fields are not required if this file is provided.')

    class Meta:
        model = Upload
        fields = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadForm, self).__init__(*args, **kwargs)
        for item in FORM_ITEMS:
            if 'id' not in item:
                continue
            help_text = item.get('docstring', '')
            label = item['label']
            if item['required']:
                label += ' *'
            if item['type'] == 'text':
                self.fields[item['id']] = forms.CharField(
                    max_length=255, label=label,
                    help_text=help_text, required=False)
            elif item['type'] == 'select':
                self.fields[item['id']] = forms.ChoiceField(
                    label=label, help_text=help_text, required=False,
                    choices=item['options'])
            elif item['type'] == 'number':
                self.fields[item['id']] = forms.DecimalField(
                    label=label, help_text=help_text, required=False)
            elif item['type'] == 'date':
                self.fields[item['id']] = forms.DateField(
                    label=label, input_formats=['%m/%d/%Y',],
                    help_text=help_text, required=False)
            self.fields[item['id']].is_list = item['list']
            if item['required']:
                add_clean_field(UploadForm, item['id'])

    def file_fields(self):
        return [self['sequence_file'], self['metadata_file']]

    def host_fields(self):
        for name in self.fields:
            if name.startswith('metadata.host'):
                yield self[name]

    def sample_fields(self):
        for name in self.fields:
            if name.startswith('metadata.sample'):
                yield self[name]
    
    def technology_fields(self):
        for name in self.fields:
            if name.startswith('metadata.technology'):
                yield self[name]

    def submitter_fields(self):
        for name in self.fields:
            if name.startswith('metadata.submitter'):
                yield self[name]

    def virus_fields(self):
        for name in self.fields:
            if name.startswith('metadata.virus'):
                yield self[name]

    def clean_metadata_file(self):
        metadata_file = self.cleaned_data['metadata_file']
        if metadata_file:
            if not qc_metadata(metadata_file.temporary_file_path()):
                raise ValidationError("Invalid metadata format")    
        return metadata_file

    def clean_sequence_file(self):
        sequence_file = self.cleaned_data['sequence_file']
        try:
            qc_fasta(sequence_file.temporary_file_path())
        except ValueError:
            raise ValidationError("Invalid file format")
        return sequence_file

    def save(self):
        self.instance = super(UploadForm, self).save(commit=False)
        self.instance.user = self.request.user
        if not self.instance.id:
            self.instance.save()
        sequence_file = self.cleaned_data['sequence_file']
        metadata_file = self.cleaned_data['metadata_file']
        if metadata_file:
            upload_to_arvados.delay(
                self.instance.id,
                sequence_file.temporary_file_path(),
                metadata_file.temporary_file_path())
        return self.instance
