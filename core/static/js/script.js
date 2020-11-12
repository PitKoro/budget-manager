function resetIncomeFilter()
{
    document.getElementById('income_select').value="";
    let form = document.getElementById('form_filter_history');
    form.submit();
}

function resetExpenceFilter()
{
    document.getElementById('expense_select').value="";
    let form = document.getElementById('form_filter_history');
    form.submit();
}

function reset_filters()
{
    document.getElementById('income_select').value="";
    document.getElementById('expense_select').value="";
    let form = document.getElementById('form_filter_history');
    form.submit();
}