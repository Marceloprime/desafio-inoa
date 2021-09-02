function setTrend(){
    rows = document.getElementsByTagName('td')

    for (variavel in rows) {

        if(rows[variavel].textContent === 'neutral'){
            rows[variavel].innerHTML = ''
        }

        if(rows[variavel].textContent=== 'up'){
            rows[variavel].innerHTML = '<svg style="color:green;align-items: center;" viewBox="0 0 24 24" width="1em" fill="none" style="height:auto" class="text-positive-main text-lg" aria-hidden="true" data-test="arrow-up"><path fill-rule="evenodd" clip-rule="evenodd" d="M18 23L18 13.7368L23 13.7368L12 0.999999L1 13.7368L6.1 13.7368L6.1 23L18 23Z" fill="currentColor"></path></svg>'
        }

        if(rows[variavel].textContent === 'down'){
            rows[variavel].innerHTML = '<svg style="color:red;" viewBox="0 0 24 24" width="1em" fill="none" style="height:auto" class="text-negative-main text-lg" aria-hidden="true" data-test="arrow-down"><path fill-rule="evenodd" clip-rule="evenodd" d="M6 1V10.2632H1L12 23L23 10.2632H17.9V1H6Z" fill="currentColor"></path></svg>'
        }

    }
}