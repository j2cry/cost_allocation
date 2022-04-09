window.addEventListener('load', () => {
    let openNotebookButton = document.getElementById('openNotebookBtn');
    openNotebookButton.onclick = () => {
        let notebookName = document.getElementById('searchInput').value;
        if (notebookName)
            window.location.href = homeURL + '/' + notebookName;
    }

    document.getElementById('searchInput').onkeydown = (ev) => {
        if (ev.key === 'Enter')
            openNotebookButton.click();
    }
})


async function request(data) {
    const response = await fetch(homeURL + '/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}
