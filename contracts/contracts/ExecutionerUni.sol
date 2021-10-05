pragma solidity ^0.7.0;
pragma abicoder v2;

import "hardhat/console.sol";
import '@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol';
import '@uniswap/v3-periphery/contracts/libraries/TransferHelper.sol';



contract Executioner {

    uint24 public constant poolFee = 3000;

    ISwapRouter public immutable swapRouter;
    
    constructor(ISwapRouter _swapRouter) {
        swapRouter = _swapRouter;
    }

    function swapExactInputSingle(uint256 amountIn, address _tokenInAddr, address _tokenOutAddr) external returns (uint256 amountOut) {
        // msg.sender must approve this contract

        // Transfer the specified amount of X token to this contract.
        TransferHelper.safeTransferFrom(_tokenInAddr, msg.sender, address(this), amountIn);

        // Approve the router to spend X token.
        TransferHelper.safeApprove(_tokenInAddr, address(swapRouter), amountIn);

        ISwapRouter.ExactInputSingleParams memory params =
            ISwapRouter.ExactInputSingleParams({
                tokenIn: _tokenInAddr,
                tokenOut: _tokenOutAddr,
                fee: poolFee,
                recipient: msg.sender,
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap.
        amountOut = swapRouter.exactInputSingle(params);
    }


    function exec_op() external view {
        console.log("Executing transaction to address: ", msg.sender);
    }
}