

async function processFiles() {
    const P4Xe_file = document.getElementById('P4Xe_file').files[0];
    const P1_file = document.getElementById('P1_file').files[0];
    const P4_file = document.getElementById('P4_file').files[0];
    const material_file = document.getElementById('material_file').files[0];

    

    const P4Xe_text = await readFile(P4Xe_file);
    // const P4Xe_text = await readFromClipboard();
    // console.log(P4Xe_text)

    const material_text = await readFile(material_file);
    const material_data = extractArticles(material_text, [1, 5, 4], ";");
    const P4Xe_data = compareArticles(extractArticles(P4Xe_text, [1, 2, 4, 5, 10, 27, 21, 22, 23], "\t"), material_data);


    // other machines
    try {
        const P1_text = await readFile(P1_file);
        const P1_data = compareArticles(extractArticles(P1_text, [1, 2, 4, 5, 10, 27, 21, 22, 23], "\t"), material_data);
        renderArticles(P1_data, "P1");
    } catch (error) {
        console.log(error)
    }
    try {
        const P4_text = await readFile(P4_file);
        const P4_data = compareArticles(extractArticles(P4_text, [1, 2, 4, 5, 10, 27, 21, 22, 23], "\t"), material_data);
        renderArticles(P4_data, "P4");
    } catch (error) {
        console.log(error)
    }

    // document.getElementById('output').textContent = JSON.stringify(P4Xe_data, null, 2);
    renderArticles(P4Xe_data, "P4Xe");
    renderReagal(material_data);


}

// function for render tables
function renderReagal(articles) {
    const container = document.getElementById("tables");
    container.innerHTML = '';
    const stationMap = {};
    articles.forEach(article => {

        let articleObject = {
            artikul: article[0],
            position: article[1],
            qty: article[2],
        };
        const stationName = article[1];
        if (articleObject.position.includes("Station") && !articleObject.artikul.includes("Leer")) {
            const sepStation = articleObject.position.split(" ");
            if (sepStation[1].length <= 2) {
                if (!stationMap[stationName]) {
                    stationMap[stationName] = [];
                }

                // Add the article and qty to the station
                stationMap[stationName].push({
                    artikul: articleObject.artikul,
                    qty: articleObject.qty,
                });
            }

        }
    })

    const sortedStations = Object.keys(stationMap).sort((a, b) => {
        const numA = parseInt(a.split(" ")[1], 10);
        const numB = parseInt(b.split(" ")[1], 10);
        return numA - numB;
    });


    sortedStations.forEach(station => {
        let materialsHTML = '';
        stationMap[station].forEach(article => {
            materialsHTML += `
                <p class="text-white-600">${article.artikul} <span class="text-red-600 font-bold">${article.qty}</span> szt</p>
            `;
        });

        const stationHTML = `
            <div class="card bg-neutral w-96 shadow-xl">
                <div class="card-body">
                    <h1 class="card-title">${station}</h1>
                    
                    <div>${materialsHTML}</div>
                </div>
            </div>
        `;

        container.innerHTML += stationHTML;
    });




}

function addPrintSpan(checkbox) {
    if (checkbox.checked) {
        var span = document.createElement("span");
        span.className = "hidden print";
        span.innerHTML = "print";
        checkbox.parentNode.appendChild(span);
    } else {
        var span = checkbox.parentNode.querySelector("span.hidden");
        if (span) {
            span.parentNode.removeChild(span);
        }
    }
}

function renderArticles(articles, id) {
    const container = document.getElementById(id);
    container.innerHTML = '';
    const work = document.getElementById("work")
    const tab = document.getElementById("P4Xe_tab")

    let timeWork = 0.0
    let qtyAll = 0

    articles.forEach(article => {
        console.log(article);
        const materialsHTML = article.materials
            .filter(material => material.article !== article.artikul)
            .filter(material => material.article.includes("E") == article.artikul.includes("E"))
            .map(material => {
                const isOnlyDigits = /^\d+$/.test(material.article);
                if (material.position.includes("Station")) {
                    article.station = true
                }
                return isOnlyDigits ? '' : `
                    <p>
                        <span class="material_name cursor-pointer text-blue-500" data-material="${material.article}">${material.article}</span> - <span class="${material.position.includes("Station") ? 'font-bold text-red-600' : 'text-yellow-600'}">${material.position}</span> - ${material.qty} szt.
                    </p>
                `;
            }).join('');
        // console.luvog(article)

        const articleHTML = `
            <div class="card w-96 shadow-xl ${article.note.length > 0 && article.note.includes("pilne") ? 'bg-yellow-300' : 'bg-base-100'}">
                <div class="card-body ${article.station ? 'bg-neutral' : 'bg-base-100'} ">
                    <div class="flex flex-col">
                    
                    <div class="flex flex-row items-center gap-2">
                        <h1 class="card-title font-weight">${article.artikul}</h1>
                        <input type="checkbox" id="myCheckbox" class="checkbox checkbox-xs" onclick="addPrintSpan(this);">
                        </div>
                    
                        
                        <span class="text-red-300 data-work">${article.dataWork}</span>
                         
       
                    </div>
                    <h4 class="description">${article.description}</h4>
                    <span class="hidden station">${article.station}</span>
                    <span class="text-red-600 text-xl font-bold note ${article.note.length > 0 && article.note.includes("pilne") ? 'text-gray-300' : ''}">${article.note}</span>
                    <div class="flex">
                        <span class="text-yellow-600 font-bold text-xl qty">${article.qty}</span>
                        <span class="text-gray-600 ml-2 p-0">szt. | </span> <span class="text-gray-600 font-bold text-xl ml-2">${article.time_work.toFixed(2)}</span>
                        
                    </div>
                    <div class="flex flex-col text-white font-bold text-md">
                        <span class="w-full amb">Wymiar: ${article.L} x ${article.B} x ${article.S}</span>
                        
                    </div>
                    <div class="divider">regal / station</div>
                    <div>
                        ${materialsHTML}
                    </div>
                </div>
            </div>
        `;
        timeWork += parseFloat(article.time_work);
        qtyAll += parseInt(article.qty)


        container.innerHTML += articleHTML;

    });

    work.innerHTML = `<strong class="text-red-300">  ${articles.length} zlecenia  ${timeWork.toFixed(2)} godziny. ${qtyAll} szt.</strong>`
    tab.setAttribute("aria-label", `P4Xe ${String(qtyAll).replace(/\n/g, ' ')}`)
    

    // document.getElementById(`${id}_tab`).setAttribute("aria-label", `${id} - ${articles.length}`);



    // Add click event listener to copy material.article to clipboard
    container.addEventListener('click', function (event) {
        if (event.target.classList.contains('cursor-pointer')) {
            const materialText = event.target.getAttribute('data-material');
            navigator.clipboard.writeText(materialText).then(() => {
                const message = document.createElement('div');

                message.classList.add('alert', 'alert-success');
                message.setAttribute("role", "alert")
                const messageContainer = document.createElement('div');
                    messageContainer.classList.add('message-container');
                message.innerHTML = `
                <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-6 w-6 shrink-0 stroke-current"
                        fill="none"
                        viewBox="0 0 24 24">
                        <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>Copied to clipboard: ${materialText} </span>
                `;


                messageContainer.appendChild(message);
                    document.body.appendChild(messageContainer);


                setTimeout(() => {
                    message.remove();
                }, 3000);

            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        }
    });
}





// functions of read file

async function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => resolve(event.target.result);
        reader.onerror = (event) => reject(event);
        reader.readAsText(file, 'ISO-8859-1');
    });
}

async function readFromClipboard() {
    return new Promise((resolve, reject) => {
        navigator.clipboard.readText().then(text => {
            // Create a TextDecoder for ISO-8859-1
            const decoder = new TextDecoder('iso-8859-1');
            
            // Decode the text
            const decodedText = decoder.decode(new TextEncoder().encode(text));
            
            // Resolve the Promise with the decoded text
            resolve(decodedText);
        }).catch(err => {
            // Reject the Promise if there is an error
            reject('Failed to read clipboard contents: ' + err);
        });
    });}

function extractArticles(text, columns, sep) {
    return text.split('\n').map(line => {
        const columnsArray = line.split(sep);
        return columns.map(index => columnsArray[index] !== undefined ? columnsArray[index] : null);
    }).filter(columns => columns.some(col => col !== null));
}

// function of compare files
function compareArticles(articles1, materials) {
    const comparisonArray = [];
    articles1.forEach(values => {
        const articleData = {
            artikul: values[0],
            description: values[1],
            qty: values[2],
            dataWork: values[3],
            note: values[4] || "",
            time_work: values[5] ? values[5].replace(",", ".") / 60 : 0,
            materials: [],
            station: false,
            L: values[6],
            B: values[7],
            S: values[8]
        };
        const splitArticles = values[0].split(/[-B]/);
        materials.forEach(material => {
            const splitMaterial = material[0].split(/[-A]/);
            if (splitArticles.some(part => part.trim() === splitMaterial[0].trim())) {
                const matchObject = {
                    article: material[0],
                    position: material[1],
                    qty: material[2]
                };
                if (material[0] != "Artikel") {
                    articleData.materials.push(matchObject);
                }
            }
        });
        comparisonArray.push(articleData);
    });
    return comparisonArray;
}
function copyMaterial(material) {
    navigator.clipboard.writeText(material).then(() => {


        console.log(material)
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

document.getElementById('P4Xe_file').addEventListener('change', processFiles);
document.getElementById('P1_file').addEventListener('change', processFiles);
document.getElementById('P4_file').addEventListener('change', processFiles);


// <span class=" ${article.note.length > 0 && article.note.includes("pilne") ? 'text-red-300' : 'text-yellow-300'}"">${article.dataWork}</span>

//  PDF
function generatePDF(id) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Select all card elements
    const container = document.getElementById(id);
    const cards = container.querySelectorAll('.card-body');
    let yOffset = 20; // Initial vertical offset for text
    doc.setFontSize(12);

    // Function to add headers
    function addHeaders() {


        doc.setFont("helvetica", "bold");
        doc.setFontSize(14);
        doc.text(`${id}`, 90, 10);
        doc.setFontSize(12);
        doc.setFont("helvetica", "normal");
        const headerY = yOffset;
        doc.text("ArtikelNr", 10, headerY);
        doc.text("Bezeichnung", 50, headerY);
        doc.text("Menge", 100, headerY);
        doc.text("Regal", 140, headerY);
        doc.line(10, headerY + 2, 190, headerY + 2); // Horizontal line below header
        yOffset += 10; // Move down for the header row
    }

    // Add initial headers
    addHeaders();

    // Loop through each card and extract data
    cards.forEach((card) => {
        const materials = card.querySelectorAll('.material_name');
        const station = card.querySelector('.station').innerText;
        // const check = card.querySelector('.print').innerText
        if (station === "false") {
            if (materials.length > 0) {
                const artikul = card.querySelector('.card-title').innerText;
                const dataWork = card.querySelector('.data-work').innerText;
                const description = card.querySelector('.description').innerText;
                const qty = card.querySelector('.qty').innerText;
                const amb = card.querySelector('.amb').innerText;


                // Truncate description if it's longer than 15 characters
                const truncatedDescription = description.length > 15 ? description.substring(0, 15) + '...' : description;
                doc.setFontSize(10);
                // Add card data to PDF in table format
                doc.setFont("helvetica", "bold");
                doc.text(artikul + "\n" + dataWork, 10, yOffset);
                doc.setFontSize(10);
                doc.setFont("helvetica", "normal");
                doc.text(truncatedDescription +'\n'+ amb, 50, yOffset);
                doc.setFontSize(12);
                doc.setFont("helvetica", "bold"); // Set font to bold
                doc.text(`${qty} szt.`, 100, yOffset);
                doc.setFont("helvetica", "normal");
                doc.setFontSize(10);

                materials.forEach((material) => {
                    const materialName = material.innerText;
                    const materialCode = material.nextElementSibling.innerText; // Assuming the code is the next sibling
                    const materialQuantity = material.parentElement.innerText.split('-').pop().trim(); // Extract quantity from the text

                    // Add material data in a structured format
                    doc.text(`${materialName}`, 125, yOffset);
                    yOffset += 5;
                    doc.text(`${materialCode}`, 125, yOffset);
                    doc.text(`${materialQuantity}`, 160, yOffset);
                    yOffset += 5; // Move down for the next material
                });
                // yOffset += 10; // Move down for the next row

                // Draw a separator line after the last material
                // yOffset += 5; // Add some space after materials
                doc.line(10, yOffset, 190, yOffset); // Horizontal line below materials
                yOffset += 5; // Move down for the next card
            }
        }


        // Add a new page if the yOffset exceeds the page height
        if (yOffset > 270) { // 270 is an arbitrary value; adjust based on your layout
            doc.addPage();
            yOffset = 20; // Reset yOffset for the new page
            addHeaders(); // Re-add headers on the new page
        }
    });

    // Save the PDF
    doc.save(`${id}.pdf`);
}


