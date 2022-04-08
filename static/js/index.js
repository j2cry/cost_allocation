window.addEventListener('load', () => {
    document.getElementById('openNotebookBtn').onclick = () => {
        let notebookName = document.getElementById('searchInput').value;
        if (notebookName)
            window.location.href = homeURL + '/' + notebookName;
    }
})