pragma solidity ^0.8.0;

contract EtherCrowd {

    uint private currentId;
    address admin;

    uint[] private crowdsalesIds;
    mapping(uint => Crowdsale) idToCrowdsale;
    uint public fee; //TODO: implement change fe function

    mapping(address => mapping(uint => uint)) balanceOf; // balance of address, crowdsale id to amount invested

    constructor(uint _fee) {
        currentId = 0;
        admin = msg.sender;
        fee = _fee;
    }



    struct Crowdsale{
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
        bool isActive;

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
            revert();
        }


        address[] memory _contributors;

        crowdsalesIds.push(currentId); // pushing the crowdsale into the crowsales list
        idToCrowdsale[currentId] = Crowdsale(
                    msg.sender,
                    currentId, // is it necessary to repead the id here?
                    _title,
                    _slogan,
                    _description,
                    _websiteUrl,
                    _thumbnailUrl,
                    _videoUrl,
                    0,
                    _goalAmount,
                    _startDate,
                    _endDate,
                    true,
                    _contributors
                );

        currentId++; // incrementing the current id

        // maybe returning the id of the crowdsale?
    }

    function getCrowdsale(uint _id) external view returns(
        address owner
        /*string memory title,
        string memory slogan,
        string memory websiteUrl,
        string memory thumbnailUrl*/
            )
        {
        require(idToCrowdsale[_id].id == _id, "No crowdsale with this id");
        Crowdsale memory crowdsale = idToCrowdsale[_id];

        /*address owner = crowdsale.owner;
        string calldata title = crowdsale.title;
        string calldata slogan = crowdsale.title;
        string calldata websiteUrl = crowdsale.websiteUrl;
        string calldata thumbnailUrl = crowdsale.thumbnailUrl;
        uint currentAmount = crowdsale.currentAmount;
        uint goalAmount = crowdsale.goalAmount;*/

        return(
            crowdsale.owner
            /*crowdsale.slogan,
            crowdsale.title,
            crowdsale.websiteUrl,
            crowdsale.thumbnailUrl*/

            );


    }







}