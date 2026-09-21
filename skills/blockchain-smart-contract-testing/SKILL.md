---
name: blockchain-smart-contract-testing
description: Use when testing smart contracts and dApps — Solidity/Foundry/Hardhat tests, fuzz and invariant testing, fork tests, gas profiling, reentrancy/overflow/access-control vulnerabilities, Slither/Echidna static and fuzz analysis, upgrade safety, oracle/MEV risks, and wallet UI flows.
license: MIT
metadata:
  category: platform
  version: "2.0"
  tags: blockchain, solidity, smart-contracts, foundry, hardhat, echidna, slither, reentrancy, invariants, web3
---

# Blockchain & Smart Contract Testing

Deployed contracts are **immutable, public and hold value**: bugs are exploited within minutes. Test far beyond happy paths.

## Layered approach
1. **Unit** (Foundry `forge test`, Hardhat + Chai): each function, revert reasons, events, access control.
2. **Fuzz**: `forge test` property fuzzing (`function testFuzz_Deposit(uint96 amt)`).
3. **Invariant / stateful fuzz**: system-wide rules that must *always* hold — e.g. `sum(balances) == totalSupply`, `solvency: assets >= liabilities`, `share price never decreases except by loss event`. (Foundry invariant tests, Echidna, Medusa.)
4. **Fork tests**: run against mainnet state (`forge test --fork-url $RPC --fork-block-number N`) for integrations (Uniswap, Chainlink, Aave).
5. **Static analysis**: `slither .`, Mythril, Aderyn; formal verification for critical logic (Certora, Halmos, SMTChecker).
6. **Gas & size**: `forge snapshot`, `forge test --gas-report`, contract size ≤ 24 KB.
7. **dApp/E2E**: Playwright + wallet stubs (Synpress) / local Anvil/Hardhat node.
8. **Audit & bounty** before mainnet; testnet soak; timelock + pause switch.

```solidity
// Foundry: fuzz + invariant sketch
function testFuzz_withdrawNeverExceedsDeposit(uint96 amt) public {
    vm.assume(amt > 0); deal(user, amt);
    vm.startPrank(user); vault.deposit{value: amt}(); vault.withdraw(amt); vm.stopPrank();
    assertEq(address(vault).balance, 0);
}
function invariant_solvent() public { assertGe(address(vault).balance, vault.totalLiabilities()); }
```
```bash
forge test -vvv --fuzz-runs 10000 && forge coverage --report lcov
slither . --exclude-informational && echidna . --contract VaultTest --config echidna.yaml
```

## Vulnerability checklist (SWC / OWASP SC Top 10)
Reentrancy (checks-effects-interactions, `ReentrancyGuard`, read-only reentrancy) · access control (`onlyOwner` missing, `tx.origin`, unprotected `initialize`) · integer issues (Solidity ≥0.8 checked; `unchecked` blocks, casting) · price-oracle manipulation/flash-loan, stale Chainlink (`updatedAt`, decimals) · front-running/MEV & slippage · signature replay (nonce, chainId, EIP-712 domain) · `delegatecall`/proxy storage collisions, upgrade auth (UUPS `_authorizeUpgrade`) · unchecked low-level call returns, ERC-20 quirks (fee-on-transfer, no-return USDT, rebasing) · DoS via unbounded loops/pull-over-push · randomness (`block.timestamp`) · rounding/donation/inflation attack on vaults (ERC-4626) · `selfdestruct` forced ETH.

## Operational
Deploy scripts tested on fork; verified source on explorer; immutable params reviewed; multisig ownership; emergency pause tested; monitoring/alerts (Forta, Tenderly); key management; frontend: chain switching, rejected tx, pending/failed states, wrong network, allowance UX, address checksum display, phishing-resistant signing text.

## Related
`fuzz-testing`, `property-based-testing`, `static-analysis-testing`, `security-testing`
