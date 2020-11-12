function change_selected_income_option()
{
    document.getElementById('income_select').value="";
    let form = document.getElementById('form_filter_history');
    form.submit();
}

function change_selected_expense_option()
{
    document.getElementById('expense_select').value="";
    let form = document.getElementById('form_filter_history');
    form.submit();
}