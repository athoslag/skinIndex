function readFiles() { 
	console.log("readFiles");

	document.addEventListener("DOMContentLoaded", initializeEntries);
}

function initializeEntries() { 
	var i;
	for (i = 1; i <= 3; i++) { 
		addEntry(i);
	}
}

function addEntry(index) { 
	console.log("execution #" + index)

	var entry = document.createElement("skin");   // Create a <button> element
	entry.href = "index.css"
	
	let image = document.createElement("img");
	image.id = "img_" + index;
	image.alt = index;
	image.src = 'src/' + index + '.jpg';
	image.style = "width: 50%";

	let button = document.createElement("button");
	// button.id = "btn_" + index;
	button.style.height = '20px';
	button.style.width= '80px';
	button.innerHtml = "Download";

	// button.type = "button";
	// button.addEventListener("onclick", downloadSkin(index));
	// button.onclick = downloadSkin(index);
	button.addEventListener ("click", function() {
	  	downloadSkin(index);
	});
	
	let p = document.createElement("p");
	p.appendChild(button);

	entry.appendChild(image);
	entry.appendChild(p);
	document.getElementById("skins").appendChild(entry);
}

function downloadSkin(index) {
	console.log("download skin #" + index);
	// document.getElementById("download").src = 'skin/'+index+'.skin';
}