const dataTable = document.getElementById('dataTable');
const sharersList = document.getElementById('sharersList');
const sharersPopup = document.getElementById('sharersPopup');
const rowPopup = document.getElementById('rowPopup');


window.addEventListener('load', async () => {
    const addRowButton = document.getElementById('addRowBtn');
    const saveButton = document.getElementById('saveBtn');
    addRowButton.removeAttribute('disabled');
    saveButton.removeAttribute('disabled');

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
        const sharers = getSharers(ev.target.value);
        if (new Set(sharers).size !== sharers.length) {
            // TODO: beautiful notification
            alert('Duplicates are not allowed in sharers list!');
            return
        }
        updateSharersPopup();
        updatePayers();
    }

    addRowButton.onclick = () => {
        // create row
        let rowElement = createRow();
        // add row
        dataTable.append(rowElement);
        window.scrollTo(0, document.body.scrollHeight);
    }

    saveButton.onclick = () => {
        // save changes
        sendUpdate();
    }

    document.getElementById('calcBtn').onclick = () => {
        // redir to calculations page
        window.location.href = homeURL + '/' + notebook + '/calc';
    }

    document.getElementById('debugBtn').onclick = () => {
        // debug
    }

    // receive data and fill table
    let data = await request({action: 'select', name: notebook});
    applyUpdate(data);
})


/* Functions */
function getSharers(value) {
    const pattern = /[\s~!@#$%^&*()+=\[\]{};:'"\\|/?,.<>]+/;
    return value.replaceAll(new RegExp(pattern, 'g'), ' ').trim().split(' ');
}

function updateSharersPopup() {
    const sharers = getSharers(sharersList.value)
    sharersPopup.innerHTML = '';
    sharers.forEach((value) => {
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
            if (!sharers.includes(value))
                elem.value = removeSharer(elem.value, value);
        })
    })
}

function updatePayers() {
    const sharers = getSharers(sharersList.value);
    // remove
    dataTable.querySelectorAll('[name=payer] option').forEach((element) => {
        if (!sharers.includes(element.value))
            element.remove();
    });
    // append
    sharers.forEach((val) => {
        dataTable.querySelectorAll('[name=payer]').forEach((element) => {
            const array = Array.from(element.options, (v) => { return v.innerText });
            if (!array.includes(val)) {
                const opt = document.createElement('option');
                opt.innerText = val;
                element.append(opt);
            }
        });
    });
}

function createRow(rowID) {
    // create row with given popups
    let rowElement = document.createElement('tr');
    rowElement.setAttribute('data-id', rowID ? rowID : '')
    rowElement.innerHTML = rowTemplateHTML;
    const payerInput = rowElement.querySelector('[name=payer]');
    const sharersInput = rowElement.querySelector('[name=sharers]');
    // fill payer options
    const sharers = getSharers(sharersList.value);
    sharers.forEach((val) => {
        const opt = document.createElement('option');
        opt.innerText = val;
        payerInput.append(opt);
    });

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

async function sendUpdate() {
    // collect data to update
    const sharers = getSharers(sharersList.value);
    let docs = [];
    let removeRows = [];
    dataTable.querySelectorAll('[data-changed],[hidden]').forEach((rowElement) => {
        let rowID = rowElement.getAttribute('data-id');
        if (rowElement.hidden) {
            if (rowID)
                removeRows.push(rowID);
            return
        }
        let rowData = {'_id': rowID ? rowID : ''};
        rowElement.querySelectorAll('input,select,textarea').forEach((inputElement) => {
            rowData[inputElement.name] = inputElement.value;
        });
        docs.push(rowData);
    });
    const data = {
        action: 'update',
        name: notebook,
        docs: docs,
        remove: removeRows,
        sharers: sharers,
    }
    // post updates
    const response = await request(data);
    let idCounter = 0;
    dataTable.querySelectorAll('[data-changed]').forEach((rowElement) => {
        rowElement.removeAttribute('data-changed');
        if (!rowElement.getAttribute('data-id') && response['ids'])
            rowElement.setAttribute('data-id', response['ids'][idCounter++]);
    });
}

function applyUpdate(data) {
    dataTable.innerHTML = '';
    // load sharers list
    sharersList.value = data['sharers'].join(' ');
    // parse docs
    data['docs'].forEach((doc) => {
        let rowID = doc['_id'];
        let rowElement = dataTable.querySelector(`[data-id="${rowID}"]`);
        if (!rowElement)
            rowElement = createRow(rowID);
        rowElement.querySelectorAll('[name]').forEach((inputElement) => {
            const value = doc[inputElement.name];
            inputElement.value = value ? value : "";
        });
        dataTable.append(rowElement);
    });
    // update UI
    updateSharersPopup();
    updatePayers();
}