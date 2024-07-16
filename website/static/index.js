function deleteSearch(searchId) {
  fetch('/delete-search', {
    method: 'POST',
    body: JSON.stringify({searchId: searchId})
  }).then((_res) => {
    window.location.href = '/';
  });
};