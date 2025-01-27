fetch('assets/file-list.json')
  .then(response => response.json())
  .then(data => {
    // 動態載入圖片
    const galleryContainer = document.getElementById('gallery-container');
    data.images.forEach(image => {
      const img = document.createElement('img');
      img.src = image.path;
      img.alt = '作品';
      galleryContainer.appendChild(img);
    });

    // 動態載入文章
    const blogList = document.getElementById('blog-list');
    data.posts.forEach(post => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = post.path;
      a.textContent = post.title;
      li.appendChild(a);
      blogList.appendChild(li);
    });
  })
  .catch(error => console.error('無法載入 JSON：', error));
