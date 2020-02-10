/*jshint esversion: 6 */
import { Controller } from "stimulus";

export default class extends Controller {
  static targets = [];

  connect() {
    $(document).ready(function(){
      // $("#reminders").select2();
    });
  }
}
