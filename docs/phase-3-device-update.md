# Phase 3: Device Update

This repo does not implement full OTA yet.

That is deliberate.

## What Comes Next

When the one-device telemetry path is stable, the next serious upgrade is Azure Device Update for IoT Hub.

## Why Not Now

Do not add OTA until:

- the agent is stable
- logging is stable
- rollback expectations are clear
- the team can recover a failed device

## Recommended Future Phase

1. Package the agent for release.
2. Version the release bundle.
3. Test update on one Pi only.
4. Add rollback instructions.
5. Expand to more devices later.

Keep the current repo focused on:

- one Pi
- one agent
- one hub
- one clean telemetry path
