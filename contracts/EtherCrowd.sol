pragma solidity ^0.8.0;

contract EtherCrowd {

    uint private currentId;
    address admin;

    mapping(uint => Crowdsale) idToCrowdsale;
    mapping(uint => mapping( address => uint)) idToBalanceOfContributors; // crowdsale id,  user address to amount invested by user address TODO: balance of function
    mapping( address => uint[] ) addressToListOfCrowdsales; // user address to list of crowdsales ids he is invested in

    uint public fee; //TODO: implement change fe function

    constructor(uint _fee) {
        currentId = 0;
        admin = msg.sender;
        fee = _fee;
    }

    struct Crowdsale{
        bool initialized;

        address owner;
        uint id;

        string title;
        string slogan;
        string description;

        string websiteUrl;
        string thumbnailUrl;
        string videoUrl;

        uint currentAmount;
        uint goalAmount;

        uint startDate; // TODO: implement
        uint endDate;
        bool isActive; // TODO ENUM: ISACTIVE; WILL BE ACTIVE; IS ENDED

        address[] contributors;
    }

    
    function createCrowdsale(
        uint _goalAmount,
        string memory _title,
        string memory _slogan,
        string memory _websiteUrl,
        string memory _videoUrl,
        string memory _thumbnailUrl,
        string memory _description,
        uint _startDate,
        uint _endDate

    ) external payable{
        require(_endDate > _startDate, "End date has to be after start date");
        //require(idToCrowdsale[currentId].id != 0, "Crowdsale id already exists"); // if two crowdsales are created at the same time and thus get the same id

        // Payment to list on EtherCrowd 
        // Person has to send the exact fee with the function call, otherwise the transaction will be reverted
        if(msg.value != fee){
            revert("Incorrect value");
        }


        address[] memory _contributors; // creating a empty array

        idToCrowdsale[currentId] = Crowdsale(
                    true, // Crowdsale is initialized
                    msg.sender,
                    currentId, // is it necessary to repead the id here?
                    _title,
                    _slogan,
                    _description,
                    _websiteUrl,
                    _thumbnailUrl,
                    _videoUrl,
                    0, // current amount 0 
                    _goalAmount,
                    _startDate,
                    _endDate,
                    true, // isActive set to true by default, will not be the case later
                    _contributors
                );

        currentId++; // incrementing the current id

        // maybe returning the id of the crowdsale?
    }

    function getCrowdsale(uint _id) external view returns(
        address owner
            )
        {
        require(idToCrowdsale[_id].initialized == true, "No crowdsale with this id");
        Crowdsale memory crowdsale = idToCrowdsale[_id];

        //TODO: add all crowdsale arguments

        return(
            crowdsale.owner
            );


    }

    /** 
    Function fund, fund a crowd,
    take a crowdid in parameter
    */
    function fund(uint _crowdId) payable external {
        require(msg.value > 0);
        require(idToCrowdsale[_crowdId].initialized, "Crowd does not exist."); 
        require(idToCrowdsale[_crowdId].isActive, "Crowd is not active");

        addressToListOfCrowdsales[msg.sender].push(_crowdId);
        idToBalanceOfContributors[_crowdId][msg.sender] += msg.value;//tester ça -> mapping est private -> creer un getter
    }




}