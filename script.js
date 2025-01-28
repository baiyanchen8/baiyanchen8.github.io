fetch('asserts/file-list.json')
  .then(response => response.json())
  .then(data => {
    // 動態載入圖片
    const galleryContainer = document.getElementById('gallery-container');

    // 根據修改時間排序圖片
    data.images.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

    // 載入已排序的圖片
    data.images.forEach(image => {
      const img = document.createElement('img');
      img.src = image.path;
      img.alt = '作品';
      galleryContainer.appendChild(img);
    });

    // 動態載入文章
    const blogList = document.getElementById('blog-list');

    // 根據修改時間排序文章
    data.posts.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

    // 載入已排序的文章
    data.posts.forEach(post => {
      const li = document.createElement('li');
    
      // 創建標題和路徑的容器
      const titlePathContainer = document.createElement('div');
      titlePathContainer.classList.add('title-path-container');
    
      // 創建標題
      const a = document.createElement('a');
      a.classList.add('a1');
      a.href = post.path;
      a.textContent = post.title;
    
      // 創建路徑
      const pathElement = document.createElement('span');
      pathElement.classList.add('path-info');
      pathElement.textContent = `路徑: ${post.path.replace('posts/html/', 'html/')}`;
    
      // 創建更新時間
      const updatedTimeElement = document.createElement('div');
      updatedTimeElement.classList.add('updated-time');
      updatedTimeElement.textContent = `最後更新時間: ${new Date(post.updated_at).toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })}`;
    
      // 添加到容器
      titlePathContainer.appendChild(a);
      titlePathContainer.appendChild(pathElement);
    
      // 添加容器到 li
      li.appendChild(titlePathContainer);
      li.appendChild(updatedTimeElement);
    
      // 添加 li 到 blogList
      blogList.appendChild(li);
    });
    
  })
  .catch(error => console.error('無法載入 JSON：', error));
