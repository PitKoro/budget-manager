let chooseForm = (value) => {
    let incomeForm = document.getElementById('main-page__income-form')
    let expenseForm = document.getElementById('main-page__expence-form')

    if (value === 'income' && incomeForm.classList.contains('invisible')) {
        incomeForm.classList.toggle('invisible')
        expenseForm.classList.toggle('invisible')
    }

    if (value === 'expense' && expenseForm.classList.contains('invisible')) {
        expenseForm.classList.toggle('invisible')
        incomeForm.classList.toggle('invisible')
    }
}