# tango-attributes-random-zero

Simple Device Server and Client to reproduce a *bug* that causes attributes to be set as 0
at apparently random times.

## Steps to reproduce

1. Register in Tango Database one `BraggBugTest` DS with instance name `test`
   with:
   - 1 device of `BraggBugTest` class, with the following name: `test/braggbugtest/1`

    ```console
    tango_admin --add-server BraggBugTest/test BraggBugTest test/braggbugtest/1
    ```
2. Start `BraggBugTest`: `python3 braggbugtest.py test`
3. Start client: `python3 braggbugclient.py`

## Result

The client fails with AssertionError after few seconds.
On the server we can see that the write value that reaches the server is a spectrum with *zero(s)* e.g.:
`newPos = [4.68897564e-310 6.94820997e-310]` while the client always writes [5.6, 7.8].
