/*jshint esversion: 6 */
import { Controller } from "stimulus";

export default class extends Controller {
  static targets = ['productSelect', 'locationSelect'];

  initialize() {
    let that = this;
    $(document).ready(function(){
      $(that.productSelectTarget).select2();
      $(that.locationSelectTarget).select2();
    });
  }
}
