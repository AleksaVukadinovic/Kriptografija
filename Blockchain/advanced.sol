// INTERFEJSI
// Definisu skup funkcija bez implementacije
// ne smeju imati konstruktore ni state variable
// ne smeju da nasledjuju druge ugovore (smeju druge interfejse), ne smeju imati implemntaciju
// sve funkcije moraju biti oznacene kao external

interface IKalkulator {
    function saberi(uint a, uint b) external pure returns (uint);
    function oduzmi(uint a, uint b) external pure returns (uint);
}

contract Kalkulator is IKalkulator {
    function saberi(uint a, uint b) external pure returns (uint) {
        return a + b;
    }

    function oduzmi(uint a, uint b) external pure returns (uint) {
        return a - b;
    }
}

contract Korisnik {
    IKalkulator public kalkulator;

    constructor(address _adresa) {
        kalkulator = IKalkulator(_adresa);
    }

    function izracunaj() external view returns (uint) {
        return kalkulator.saberi(10, 5);
    }
}


// INTERAKCIJA SA DRUGIM UGOVORIMA NA MREZI
// INTERAKCIJA PUTEM DIREKTNOG POZIVA

interface ICiljniUgovor {
    function getValue() external view returns (uint);
}

contract Pozivalac {
    function citajVrednost(address _ciljnaAdresa) external view returns (uint) {
        return ICiljniUgovor(_ciljnaAdresa).getValue();
    }
}

// NASLEDJIVANJE

contract Zivotinja {
    string public ime;

    constructor(string memory _ime) {
        ime = _ime;
    }

    function jedi() public pure virtual returns (string memory) {
        return "Zivotinja jede";
    }
}

contract Macka is Zivotinja {
    constructor(string memory _ime) Zivotinja(_ime) {}

    function jedi() public pure override returns (string memory) {
        return "Macka jede hranu";
    }

    function zvuk() public pure returns (string memory) {
        return "mjau";
    }
}

// Modifikator	Dostupno spolja?	Dostupno iz naslednika?	    Dostupno unutar ugovora?
// public	            ✅	                ✅	                        ✅
// external	            ✅	                ❌ (samo sa this.)	        ❌
// internal	            ❌	                ✅	                        ✅
// private	            ❌	                ❌   	                    ✅

// ERC20 je najrasprostranjeniji standard za fungibilne (zamenjive) tokene na Ethereum mreži.
// Definisao je uniformni interfejs koji svaki token mora da implementuje kako bi bio kompatibilan sa novčanicima, berzama i dApps-ovima.

// FALLBACK I RECEIVE FUNKCIJE

// receive - Poziva se kada ugovor primi čist ETH transfer (bez calldata). Mora biti external payable.

contract PrimaocETH {
    event PrimljenETH(address posiljalac, uint iznos);

    // Poziva se kada se ETH pošalje direktno na ugovor (bez podataka)
    receive() external payable {
        emit PrimljenETH(msg.sender, msg.value);
    }
}

// fallback - Poziva se u dva slučaja: 1. Kada se pozove funkcija koja ne postoji u ugovoru 2. Kada se ETH pošalje sa podacima (msg.data nije prazno)

contract SvePrihvata {
    event FallbackPokrenut(address posiljalac, uint vrednost, bytes podaci);

    // Poziva se za nepostojeće funkcije ili ETH + calldata
    fallback() external payable {
        emit FallbackPokrenut(msg.sender, msg.value, msg.data);
    }
}

// Kombinovano

contract KombinovaniPrimaoc {
    uint public ukupnoPrimljeno;
    mapping(address => uint) public uplate;

    // Čist ETH transfer
    receive() external payable {
        ukupnoPrimljeno += msg.value;
        uplate[msg.sender] += msg.value;
    }

    // Pogrešan potpis funkcije ili ETH sa podacima
    fallback() external payable {
        // Možemo logirati ili odbiti neprepoznate pozive
        ukupnoPrimljeno += msg.value;
    }
}

// Re-Entrancy napad - jedan od najopasnijih napada u Solidity-ju.
// Napadač eksploatiše redosled operacija u funkciji - posebno kada ugovor salje ETH pre nego sto azurira stanje

// Kako funkcioniše napad
// Napadač poziva withdraw() na žrtvinom ugovoru
// Žrtvin ugovor šalje ETH napadaču
// Pre nego što žrtvin ugovor ažurira balans — napadačev receive() se poziva
// receive() PONOVO poziva withdraw() na žrtvinom ugovoru
// Žrtvin ugovor misli da napadač još uvek ima balans (nije ažuriran)
// Ciklus se ponavlja dok žrtvin ugovor nema više ETH
