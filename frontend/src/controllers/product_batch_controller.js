/*jshint esversion: 6 */
import { Controller } from "stimulus";

export default class extends Controller {
  static targets = ['productSelect'];

  initialize() {
    let that = this;
    $(document).ready(function(){
      $(that.productSelectTarget).select2();
    });
  }
}
