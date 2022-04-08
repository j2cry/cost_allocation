const dataTable = document.getElementById('dataTable');
const sharersList = document.getElementById('sharersList');
const sharersPopup = document.getElementById('sharersPopup');
const rowPopup = document.getElementById('rowPopup');


window.addEventListener('load', () => {

    window.onclick = (ev) => {
        if (ev.target.name !== 'sharers')
            sharersPopup.hidden = true;
        rowPopup.hidden = true;
    }

    sharersPopup.onclick = (ev) => {
        ev.stopPropagation();
    }

    sharersList.onchange = (ev) => {
        // on sharers list changed
        let pattern = /[\s~!@#$%^&*()+=\[\]{};:'"\\|/?,.<>]+/;
        let sharers = ev.target.value.replaceAll(new RegExp(pattern, 'g'), ' ').trim().split(' ');
        if (new Set(sharers).size !== sharers.length) {
            // TODO: beautiful notification
            alert('Duplicates are not allowed in sharers list!');
            return
        }
        updateSharersPopup(sharers);
    }

    document.getElementById('addRowBtn').onclick = () => {
        // create row
        let rowElement = createRow(rowPopup, sharersPopup);
        // add row
        dataTable.append(rowElement);
        window.scrollTo(0, document.body.scrollHeight);
    }

    document.getElementById('calcBtn').onclick = () => {
        // TODO: request for results and display in overlay
        window.location.href = homeURL + '/' + notebook + '/calc';
    }

    document.getElementById('debugBtn').onclick = () => {
        sendUpdate();
    }

    // TODO: receive data and fill table
    applyUpdate({});
})


/* Functions */
function updateSharersPopup(list) {
    sharersPopup.innerHTML = '';
    list.forEach((value) => {
        // const elemID = value + 'Checkbox';
        const elemID = value;
        const sharer = document.createElement('div');
        sharer.innerHTML = sharerHTML;
        sharer.querySelector('input').setAttribute('id', elemID)
        const label = sharer.querySelector('label');
        label.innerText = value;
        label.setAttribute('for', elemID);
        sharersPopup.append(sharer);
    })
    // clean sharers inputs: remove item if it was removed from sharers list
    document.querySelectorAll('[name=sharers]').forEach((elem) => {
        let oldSharers = elem.value.split(' ');
        oldSharers.forEach((value) => {
            if (!list.includes(value))
                elem.value = removeSharer(elem.value, value);
        })
    })
}

function createRow(rowPopup, sharersPopup, rowID) {
    // create row with given popups
    let rowElement = document.createElement('tr');
    rowElement.setAttribute('data-id', rowID ? rowID : '')
    rowElement.innerHTML = rowTemplateHTML;
    let sharersInput = rowElement.querySelector('[name=sharers]');
    // init and show row context menu
    rowElement.oncontextmenu = (ev) => {
        ev.preventDefault();
        sharersPopup.hidden = true;
        rowPopup.style.left = ev.pageX.toString() + 'px';
        rowPopup.style.top = ev.pageY.toString() + 'px';
        let removeBtn = rowPopup.querySelector('#removeRowBtn')
        removeBtn.onclick = () => {
            // set remove flag
            rowElement.hidden = true;
            rowPopup.toggleAttribute('hidden');
        }
        rowPopup.toggleAttribute('hidden');
    }
    // onchange any row input
    rowElement.querySelectorAll('input,select,textarea').forEach((inputElement) => {
        inputElement.onchange = () => {
            rowElement.setAttribute('data-changed', '');
        }
    });
    // update and show sharers list
    sharersInput.onmousedown = (ev) => {
        ev.preventDefault();
        // set position
        let rect = ev.target.getBoundingClientRect();
        sharersPopup.style.left = rect.x.toString() + 'px';
        sharersPopup.style.top = (rect.y + rect.height).toString() + 'px';
        sharersPopup.style.width = rect.width.toString() + 'px';
        sharersPopup.querySelectorAll('input[type=checkbox]').forEach((checkbox) => {
            // update sharers list with info from actual row
            let selected = sharersInput.value.split(' ');
            checkbox.checked = selected.includes(checkbox.id);
            checkbox.onchange = () => {
                // change value on checked switch
                if (checkbox.checked) {
                    let selected = sharersInput.value ? sharersInput.value.split(' ') : [];
                    selected.push(checkbox.id);
                    sharersInput.value = selected.join(' ');
                } else {
                    sharersInput.value = removeSharer(sharersInput.value, checkbox.id);
                }
                sharersInput.onchange();
            }
        })
        // show sharers popup
        sharersPopup.toggleAttribute('hidden');
    }
    return rowElement
}

function removeSharer(value, sharer) {
    let pat = new RegExp(`\\s*${sharer}\\s*`, 'g');
    return value.replaceAll(pat, ' ').trim();
}

function sendUpdate() {
    // collect data to update
    let data = {};
    let counter = 0;
    let removeRows = [];
    dataTable.querySelectorAll('[data-changed],[hidden]').forEach((rowElement) => {
        let rowID = rowElement.getAttribute('data-id');
        let rowData = {};
        if (rowElement.hidden) {
            if (rowID)
                removeRows.push(rowID);
            return
        }
        rowElement.querySelectorAll('input,select,textarea').forEach((inputElement) => {
            rowData[inputElement.name] = inputElement.value;
        });
        data[rowID ? rowID : 'new' + counter++] = rowData;
    });
    data['remove'] = removeRows;
    // post
    console.log(data);
}

function applyUpdate(data) {
    dataTable.innerHTML = '';
    // load sharers list
    let sharers = ['foo', 'boo', 'bar'];        // debug data
    sharersList.value = sharers.join(' ');
    let count = 20;
    for (let i = 0; i < count; i++) {
        dataTable.append(createRow(rowPopup, sharersPopup, i + 1));
    }

    updateSharersPopup(sharers);
}