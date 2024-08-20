document.addEventListener("DOMContentLoaded", () => {
    const posts = window.posts;
    const likes = window.likes;
    const users = window.users;
    const currentUsername = window.current_user;
    const currentUserPk = users.find(user => user.fields.username === currentUsername).pk;

    
    posts.forEach( post => {
        const author_username = users.find(user => user.pk == post.fields.user)
                                        .fields.username;
        
        const date = new Date(post.fields.date);
        let isAuthor = currentUsername == author_username;

        let number_of_likes = likes.filter(like => like.fields.post === post.pk).length;
        let likesForPostByUser = likes.filter(like => like.fields.post === post.pk && currentUserPk === like.fields.user);
        let isLiked = likesForPostByUser.length > 0;
        let liked = isLiked ? "Unlike": "Like";


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
        

        const likeButton = document.createElement("button");
        likeButton.classList.add("like-button");
        likeButton.setAttribute("id", `like-${post.pk}`);
        likeButton.textContent = liked;
        newPost.appendChild(likeButton);

        likeButton.addEventListener("click", () => {
            isLiked = !isLiked;
            likeButton.textContent = isLiked ? "Unlike": "Like";

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch(`/edit_post`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    isLiked: !isLiked,
                    id: post.pk,
                    user: currentUserPk
                })
            }).then(response => {
                const likesDiv = document.getElementById(`likes-${post.pk}`);
                var likesCount = likesDiv.textContent.trim();
                likesCount = Number(likesCount.replace(/[^0-9]/g, ''));
                likesCount = isLiked? likesCount + 1 : likesCount - 1;
                likesDiv.textContent = `❤️${likesCount}`;
            });

        });
    
        
        if(isAuthor){
            const editButton = document.createElement("button");
            editButton.classList.add("edit-button");
            editButton.setAttribute("id", post.pk);
            editButton.textContent = "Edit";
            newPost.appendChild(editButton);
            editButton.addEventListener("click", () => {
                editButton.style.visibility = "hidden";

                let currentText = document.getElementById(`post-${editButton.id}`).textContent;
                const divToEdit = document.getElementById(`div-${editButton.id}`);
                divToEdit.innerHTML = `<textarea class="edit-textarea" id="edit-${editButton.id}">${currentText}</textarea>`;
                
                
                
                const saveButton = document.createElement("button");
                saveButton.textContent = "Save";
                saveButton.classList.add("edit-button");
                saveButton.style.textAlign = "center";
                newPost.appendChild(saveButton);
                saveButton.addEventListener("click", () => {
                    editButton.style.visibility = "visible";
                    saveButton.style.visibility = "hidden";
                    let newPostText = document.getElementById(`edit-${editButton.id}`).value;
                    divToEdit.innerHTML = `<h4 class="text-content" id="post-${post.pk}">${newPostText}</h4>`;
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    fetch(`/edit_post`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({
                            newText: newPostText,
                            id: post.pk
                        })
                    })


            });
        });
        
    }
        document.querySelector("#posts").appendChild(newPost);
    });

});
