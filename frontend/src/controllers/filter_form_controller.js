/*jshint esversion: 6 */
import { Controller } from "stimulus";

export default class extends Controller {
  static targets = [];

  initialize() {
    $(document).ready(function(){
      $("#id_store").select2();
      $("#id_product").select2();
    });
  }
}
