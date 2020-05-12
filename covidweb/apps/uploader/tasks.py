from celery import task

@task
def upload_to_arvados(upload_pk, sequence_file, metadata_file):
    pass
