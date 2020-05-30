from api.models import ProductBatch, BatchWarning, ProductBatchArchive


class BatchController:

    @classmethod
    def update_batch(cls, batch_id, new_quantity):
        batch = ProductBatch.get_by_id(batch_id)
        batch.update_quantity(new_quantity)
        if new_quantity == 0:
            batch_archive = ProductBatchArchive.create_batch_archive(batch)
            BatchWarning.archive_warnings(batch.id, batch_archive.id)
            batch.delete()

    @classmethod
    def update_warnings(cls, batch_id, new_quantity):
        BatchWarning.silence_warnings(batch_id, new_quantity)

