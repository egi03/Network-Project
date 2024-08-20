document.addEventListener("DOMContentLoaded", () => {
    const posts = window.posts;
    const likes = window.likes;
    const users = window.users;
    
    posts.forEach( post => {
        const author_username = users.find(user => user.pk == post.fields.user)
                                        .fields.username;
        
        const date = new Date(post.fields.date);

        let number_of_likes = likes.filter(like => like.fields.post === post.pk).length;

        const newPost = document.createElement("div");
        newPost.classList.add("single-post");
        newPost.innerHTML = `
        <a href="/profile/${author_username}">${author_username}</a>
        <div id="div-${post.pk}">
        <h4 class="text-content" id="post-${post.pk}">${post.fields.content}</h4>
        </div>
        <p class="post-date">${date.toDateString()}</p>
        <div id="likes-${post.pk}" class="likes">❤️${number_of_likes}
        </div>`;
        
        document.querySelector("#posts").appendChild(newPost);
    });

});
