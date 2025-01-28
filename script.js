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
      
      // 創建標題
      const a = document.createElement('a');
      a.classList.add('a1'); 

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
      const pathElement = document.createElement('div');
      pathElement.classList.add('path-info'); // 加入 path-info 類別
      pathElement.textContent = `路徑: ${formattedPath}`;

      const updatedTimeElement = document.createElement('span');
      updatedTimeElement.classList.add('updated-time');
      updatedTimeElement.textContent = `最後更新時間: ${updatedTime}`;

      const tmp = document.createElement('div');
      tmp.classList.add('tmp1');
      const info=document.createElement('div');
     info.classList.add('taJustify');
     info.appendChild(a);
     info.appendChild(tmp);
     info.appendChild(pathElement); 
      // 只在 CSS 中進行排版調整，不改動 li 結構
      li.appendChild(info); // 把標題加到 li 裡
      li.appendChild(updatedTimeElement); // 把更新時間加到 li 裡

      // 把列表項目加入 blogList
      blogList.appendChild(li);
    });
  })
  .catch(error => console.error('無法載入 JSON：', error));
