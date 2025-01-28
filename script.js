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
      const a = document.createElement('a');
      a.href = post.path;
      a.textContent = post.title;

      // 顯示修改時間，格式化為中文時間
      const updatedTime = new Date(post.updated_at).toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });

      // 將完整路徑轉換為相對路徑格式
      const formattedPath = post.path.replace('posts/html/', 'html/');
      const pathElement = document.createElement('span');
      pathElement.classList.add('path-info'); // 加入 path-info 類別
      pathElement.textContent = `路徑:  ${formattedPath}`;
      pathElement.style.display = 'block'; // 顯示為區塊，換行

      const updatedTimeElement = document.createElement('span');
      updatedTimeElement.classList.add('updated-time');
      updatedTimeElement.textContent = `最後更新時間: ${updatedTime}`;

      const infoContainer = document.createElement('div');
      infoContainer.classList.add('info-container'); // 容器類別
      
      infoContainer.appendChild(pathElement); // 將路徑資訊加入容器
      infoContainer.appendChild(updatedTimeElement); // 將更新時間加入容器
      
      // 把文章標題和右側資訊加入到 list item
      li.appendChild(a); // 標題
      li.appendChild(infoContainer); // 右側資訊容器
      blogList.appendChild(li);
      
    });
  })
  .catch(error => console.error('無法載入 JSON：', error));
