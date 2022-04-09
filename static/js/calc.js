window.addEventListener('load', () => {
    const personalCalc = document.getElementById('personalCalcFor');
    const personalTable = document.getElementById('personalTable');
    personalCalc.onchange = async (ev) => {
        personalTable.innerHTML = '';
        const data = await request({action: 'calc', name: notebook, person: ev.target.value});
        Object.entries(data).forEach(([rowName, value]) => {
            const rowElement = document.createElement('tr');
            // console.log(rowName, value['expenses'], value['payments'])
            rowElement.append(createCell('py-1', rowName));
            rowElement.append(createCell('py-1', value['expenses']));
            rowElement.append(createCell('py-1', value['payments']));
            personalTable.append(rowElement);
        });
    }
    personalCalc.dispatchEvent(new Event('change'));
})

function createCell(cls, text) {
    const cell = document.createElement('td');
    cell.classList.add(cls);
    cell.innerText = text;
    return cell
}