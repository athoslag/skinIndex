var loadedItems = 1670;

function readFiles() { 
	console.log("readFiles");

	document.addEventListener("DOMContentLoaded", initializeEntries);
}

function initializeEntries() { 
	loadMoreEntries(30)
}

function loadMoreEntries(offset) { 
	var i;
	let loaded = loadedItems;

	for (i = loaded ; i <= loaded + offset; i++) { 
		addEntry(i);
		loadedItems += 1;
	}
}

function addEntry(index) { 
	console.log("execution #" + index);

	var entry = document.createElement("skin");
	let title = document.createElement("p");
	let image = document.createElement("img");
	let button = document.createElement("button");

	// Title

	title.textContent = 'Skin #' + index + ':';
	title.style.fontWeight = 'bold';
	title.style.textAlign = 'left';

	entry.appendChild(title);
	
	// Image

	image.id = "img_" + index;
	image.alt = index;

	image.onload = function() {
  		image.width = this.width * 0.5;
	}

	image.onerror = function() { 
		image.src = 'src/placeholder.jpg';
		image.width = 400;
		button.disabled = true;
		console.log('Error loading image #' + index);

		button.style.backgroundColor  = 'lightgray';
	};

	let imageURL = 'image/' + index + '.jpg';
	image.src = imageURL;

	// Button

	button.setAttribute('id', 'btn' + index);
	button.textContent = 'Download #' + index;

	button.addEventListener ("click", function() {
	  	downloadSkin(index);
	  	button.textContent = 'Downloaded!'
	});
	
	let p = document.createElement("p");
	p.appendChild(button);

	// Entry elements

	entry.style.backgroundColor = "lightgreen";
	entry.appendChild(image);
	entry.appendChild(p);
	document.getElementById("skins").appendChild(entry);
}

function downloadError() { 
}

function downloadSkin(index) {
	let baseUrl = 'skin/' + index;
	let skinUrl = baseUrl + '.skin';
	let hshinUrl = baseUrl + '.hskin';

	let downloader = document.getElementById("download");
	downloader.onerror = function() { 
		downloader.src = hskinUrl;
	};

	downloader.src = skinUrl;
}