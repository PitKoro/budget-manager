function resetIncomeFilter() {
    document.getElementById('category-filter__income').value="";
}

function resetExpenseFilter() {
    document.getElementById('category-filter__expense').value="";
}

function applyActionsAndSubmit(actions) {
    actions.forEach(action => {
        action()
    });
    document.getElementById('history-page__month-and-categories-filter').submit();
}