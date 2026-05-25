Feature: cross-platform directory synchronization tool (aros-sync)
  As an AROS Pipeline administrator or agent script
  I want to run a native, compiled synchronization CLI
  In order to safely sync Skills, KIs, Workflows, and Policies across targets without shell scripts

  Scenario: Synchronize changed Skill to local runtime environment
    Given the aros-sync CLI is compiled and available
    And a local modified Skill directory in the Factory "Skills/my-skill"
    When I run "aros-sync push --target ~/.gemini/skills/my-skill"
    Then the target directory should match the source content hashes
    And the operation should be logged in SHARED_ASSET_REGISTRY.md

  Scenario: Safe cross-platform folder lock fallback on concurrency collisions
    Given another instance of aros-sync holds the lock file "knowledge.lock"
    When I run "aros-sync push" in parallel
    Then the second run should wait for release using atomic retry backoffs
    And if lock times out it should report a lock contention error (status 1)
