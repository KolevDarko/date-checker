/*jshint esversion: 6 */
import { Controller } from "stimulus";

export default class extends Controller {
  static targets = [];

  initialize() {

  }

  editBatch(evt){
    let $parentRow = $(evt.target).closest('tr');
    let batchId = $parentRow.data('batchId');
    let batchUrl = BASE_URL + '/dash/product-batch-list/' + batchId;
    window.location = batchUrl;
  }

}
