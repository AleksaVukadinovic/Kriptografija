// TIPOVI

contract tipovi {
    bool public boolean;
    uint256 public unsigned_integer;
    int256 public signed_integer;
    address public adresa;

    // keyword public znaci da polje ima podrazumevani getter
    // ne znaci da bilo ko moze da promeni promenljivu
}


// PROMENLJIVE

contract promenljive {

    // 1) PROMENLJIVE STANJA: cuvaju se na blockchainu, placamo gas za njihovo odrzavanje
    bool proba;
    address nesto;

    function test() public view {
        // 2) LOKALNE PROMENLJIVE: postoje samo tokom izvrsavanja funkcije, ne placamo gas za njihovo odrzavanje
        uint broj;
        address neko;
    }

    // 3) GLOBALNE PROMENLJIVE: ne deklarisu se, imaju podatke o blockchainu, uvek postoje i placaju se
    msg.sender // ovo je adresa vlasnika ugovora
    msg.value
    block.blockhash
}

// KONTROLA TOKA - grananja, petlje

contract kontrola_toka {
    function test() public pure {
        for (uint i = 0; i < 10; i++) {
            if (i % 3 == 1) continue;
            else if (i == 7) break;
        }
    }
}

// NAPREDNIJI TIPOVI PODATAKA

contract struktura {

    struct student {
        string ime;
        uint polozenoESPB;
    }

    uint[] public niz;   // niz dinamicke duzine
    uint[3] public niz2; // niz fiksne duzine 3

    mapping (uint => uint) public tranformacija; // kljuc -> vrednost, nije iterabilan

    student[] private studenti;
    mapping (address => student) public nesto; // mapping ne dozvoljava strukturu kao kljuc

    function dodaj (uint _a) public {
        tranformacija[_a] = (_a + 7) * 57 % 23;
        niz.push(_a);
    }

    function suma() public view returns(uint) {
        uint s = 0;
        uint i;
        for (i = 0; i < niz.length; i++) {
            s += niz[i];
        }
        return s;
    }
}


// FUNKCIJE I MODIFIKATORI

contract PetStore {

    struct Pet{
        string ime;
        uint id;
        uint cena;
        address vlasnik;
        bool naprodaju;
    }

    uint broj;
    uint id;
    address public vlasnik;

    mapping (uint => Pet) public ljubimci;

    event AddedPet(string _ime, uint cena);
    event PetBought(uint _id);

    constructor(){
        broj = 0;
        id = 0;
        vlasnik = msg.sender;
    }

    modifier samoVlasnik(){
        require(vlasnik == msg.sender,"samo vlasnik sme da radi ovo");
        _;
    }

    function addPet(string memory _ime, uint _cena) public samoVlasnik{
        _dodaj(_me,_cena);
        emit AddedPet(_ime,_cena);
    }

    function _dodaj(string memory _ime, uint _cena) private{
        address _a;
        _cena = _cena ;
        Pet memory _pet = Pet(_ime,id,_cena,_a,true);
        ljubimci[id]= _pet;
        id += 1;
        broj += 1;
    }

    function buyPet(uint _id) public payable returns(bool){
        require(ljubimci[_id].naprodaju,"Nije na prodaju");
        require(msg.value == ljubimci[_id].cena, "nisi poslao tacno koliko treba" );
        ljubimci[_id].vlasnik = msg.sender;
        ljubimci[_id].naprodaju = false;
        broj -=1;
        emit PetBought(_id);
        return true;
    }

    function getPet(uint _id) public view returns(Pet memory){
       return ljubimci[_id];
    }

}
