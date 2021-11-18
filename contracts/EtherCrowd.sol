pragma solidity ^0.8.0;
import "../interfaces/KeeperCompatibleInterface.sol";
import "./ReentrancyGuard.sol";

contract EtherCrowd is KeeperCompatibleInterface, ReentrancyGuard {
    uint256 public nbOfProjects;
    address admin;

    uint256 public checkInterval;
    uint256 public lastCheck;

    mapping(uint256 => Project) private idToProject;

    // crowdsale id,  user address to amount invested by user address TODO: balance of function
    mapping(uint256 => mapping(address => uint256))
        private idToBalanceOfContributors;

    // user address to list of crowdsales ids he is invested in
    mapping(address => uint256[]) private addressToListOfProjects;

    uint256 public fee; //TODO: implement change fe function

    constructor(uint256 _fee, uint256 _checkInterval) {
        nbOfProjects = 0;
        admin = msg.sender;
        fee = _fee;
        checkInterval = _checkInterval;
        lastCheck = 0;
    }

    enum Status {
        NOT_STARTED,
        ACTIVE,
        ENDED
    }

    struct Project {
        bool initialized;
        address owner;
        uint256 id;
        string title;
        string slogan;
        string description;
        string websiteUrl;
        string thumbnailUrl;
        string videoUrl;
        uint256 currentAmount;
        uint256 goalAmount;
        //TODO implement themes

        uint256 startDate; // TODO: implement
        uint256 endDate;
        Status status;
        address[] contributors;
    }

    function createProject(
        uint256 _goalAmount,
        string memory _title,
        string memory _slogan,
        string memory _websiteUrl,
        string memory _videoUrl,
        string memory _thumbnailUrl,
        string memory _description,
        //  no need to specify start date, it is the time at which the user calls the function
        uint256 _endDate
    ) external payable {
        require(_goalAmount > 0, "Goal amount must be greater than zero.");
        require(_endDate > 0, "End date has to be after start date.");
        //require(idToCrowdsale[nbOfProjects].id != 0, "Crowdsale id already exists"); // if two crowdsales are created at the same time and thus get the same id

        // Payment to list on EtherCrowd
        // Person has to send the exact fee with the function call, otherwise the transaction will be reverted
        if (msg.value != fee) {
            revert("Incorrect value");
        }

        address[] memory _contributors; // creating a empty array

        idToProject[nbOfProjects] = Project(
            true, // Crowdsale is initialized
            msg.sender,
            nbOfProjects, // is it necessary to repead the id here?
            _title,
            _slogan,
            _description,
            _websiteUrl,
            _thumbnailUrl,
            _videoUrl,
            0, // current amount 0
            _goalAmount,
            block.timestamp, // start date
            block.timestamp + _endDate,
            Status.ACTIVE, // Project is active by default, later implementation will make possible an activation at a later date
            _contributors
        );

        nbOfProjects++; // incrementing the current id

        // maybe returning the id of the crowdsale?
    }

    // Modifiers
    modifier projectExist(uint256 _id) {
        require(
            idToProject[_id].initialized == true,
            "Project does not exist."
        );
        _;
    }

    modifier projectNotStarted(uint256 _id) {
        require(
            idToProject[_id].status == Status.NOT_STARTED,
            "Project must be not started."
        );
        _;
    }

    modifier projectActive(uint256 _id) {
        require(
            idToProject[_id].status == Status.ACTIVE,
            "Project is not active."
        );
        _;
    }

    modifier projectEnded(uint256 _id) {
        require(
            idToProject[_id].status == Status.ENDED,
            "Project is not ended."
        );
        _;
    }

    //If we have this modifier should we need the previous one ???
    modifier projectExpired(uint256 _id) {
        require(
            idToProject[_id].endDate <= block.timestamp,
            "Project is not yet expired."
        );
        _;
    }

    /**
     * @dev Gets the project of the given id.
     * @param _id The id of the project.
     * @return project The project.
     */
    function getProject(uint256 _id)
        external
        view
        projectExist(_id)
        returns (Project memory)
    {
        Project memory project = idToProject[_id];

        return (project);
    }

    //TODO Maybe return only active and not started project.
    /**
     * @dev Gets all the projects (not_started, active or ended).
     * @return projects a list of projects.
     */
    function getProjects() external view returns (Project[] memory) {
        Project[] memory projects = new Project[](nbOfProjects);

        for (uint256 i = 0; i < nbOfProjects; i++) {
            projects[i] = idToProject[i];
        }
        return projects;
    }

    // ChainLink UpKeep part, maybe putting it in another file?

    function checkUpkeep(
        bytes calldata /*checkData*/
    )
        external
        view
        override
        returns (
            bool upkeepNeeded,
            bytes memory /*performData*/
        )
    {
        // This function will be executed Off chain by the Keeper node, this is why the computation is done here in order to save on gas fees
        upkeepNeeded = (block.timestamp - lastCheck) > checkInterval;
        // We don't use the checkData in this example. The checkData is defined when the Upkeep was registered.
    }

    function performUpkeep(
        bytes calldata /*performData*/
    ) external override {
        lastCheck = block.timestamp;
        checkProjects();

        // We don't use the performData in this example. The performData is generated by the Keeper's call to your checkUpkeep function
    }

    function checkProjects() private {
        for (uint i = 0; i < nbOfProjects; i++) {
            Project storage project = idToProject[i];

            // Project ended
            if (
                project.status == Status.ACTIVE &&
                block.timestamp >= project.endDate
            ) {
                endProject(project.id);
            }
        }
    }

    function endProject(uint _projectId)
        private
        projectExist(_projectId)
        projectActive(_projectId)
        projectExpired(_projectId)
    {
        Project storage _project = idToProject[_projectId];
        // Goal reached
        if (_project.currentAmount >= _project.goalAmount) {
            payable(_project.owner).transfer(_project.currentAmount);
        } else {
            refund(_project.id);
        }

        // End the project
        _project.status = Status.ENDED;
    }

    function refund(uint _projectId)
        private
        projectExist(_projectId)
        projectActive(_projectId)
        projectExpired(_projectId)
        nonReentrant
    {
        Project storage _project = idToProject[_projectId];

        for (uint i = 0; i < _project.contributors.length; i++) {
            // Refund
            address contributorAddress = _project.contributors[i];
            uint refundAmount = idToBalanceOfContributors[_project.id][
                contributorAddress
            ];

            // Reset balance
            idToBalanceOfContributors[_project.id][
                contributorAddress
            ] -= refundAmount;

            payable(contributorAddress).transfer(refundAmount);

           
        }
    }

    /** 
    Function fund, fund a crowd,
    takes a crowdid in parameter
    */
    function fund(uint256 _projectId) external payable {
        require(msg.value > 0, "No value sent.");
        require(idToProject[_projectId].initialized, "Project does not exist.");
        require(
            idToProject[_projectId].status == Status.ACTIVE,
            "Project is not active"
        );

        addressToListOfProjects[msg.sender].push(_projectId);
        idToBalanceOfContributors[_projectId][msg.sender] += msg.value;
        // Adding user to adress of contibutors of the project when fund
        idToProject[_projectId].contributors.push(msg.sender);
    }

    function getInvestedFunds(uint256 _projectId)
        public
        view
        returns (uint256 balance)
    {
        require(idToProject[_projectId].initialized, "Project does not exist.");
        return idToBalanceOfContributors[_projectId][msg.sender];
    }
}
