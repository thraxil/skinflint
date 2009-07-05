function update_budgets() {
  var total = parseInt($('total-income').value);
  var used = 0;
  var remainder = parseInt($('income-Remainder').value);
  forEach(getElementsByTagAndClassName('input','budget'),
    function (budget) {
      used += parseInt(budget.value);
    }
    );
  if ((total - used) > 0) {
    $('messages').value  = "surplus " + (total - used);
    $('income-Remainder').value  = remainder + (total - used);
  }
  if ((total - used) < 0) {
    $('messages').value = "over by " + (used - total);
  }
}
