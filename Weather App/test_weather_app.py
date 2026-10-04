"""
Automated tests using mocked API responses (no internet or real key needed).
Run:  python test_weather_app.py
"""
import io
import contextlib
import os
import unittest
from unittest import mock

import requests
import weather_app as wa

GOOD = {"name": "London", "sys": {"country": "GB"},
        "main": {"temp": 20.0, "humidity": 60},
        "weather": [{"description": "light rain"}], "wind": {"speed": 3.5}}


class FakeResponse:
    def __init__(self, status=200, payload=None, bad_json=False):
        self.status_code, self._payload, self._bad = status, payload, bad_json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(response=self)
    def json(self):
        if self._bad:
            raise ValueError("not json")
        return self._payload


def fetch(response=None, side_effect=None):
    with mock.patch("weather_app.requests.get", return_value=response, side_effect=side_effect) as g:
        return wa.fetch_weather("London", "KEY"), g


def run_main(inputs, responses):
    out = io.StringIO()
    with mock.patch.dict(os.environ, {"OPENWEATHER_API_KEY": "KEY"}), \
         mock.patch("builtins.input", side_effect=inputs), \
         mock.patch("weather_app.requests.get", side_effect=responses), \
         contextlib.redirect_stdout(out):
        wa.main()
    return out.getvalue()


class Tests(unittest.TestCase):
    def test1_valid_city(self):
        (data, err), g = fetch(FakeResponse(200, GOOD))
        self.assertIsNone(err); self.assertEqual(data["name"], "London")
        self.assertEqual(g.call_args.kwargs["params"]["q"], "London")
        self.assertEqual(g.call_args.kwargs["params"]["units"], "metric")
        self.assertEqual(g.call_args.kwargs["timeout"], wa.TIMEOUT_SECONDS)

    def test2_zip_code(self):
        p = wa.build_request_params("94040, US", "KEY")
        self.assertEqual(p["zip"], "94040,US"); self.assertNotIn("q", p)

    def test3_city_not_found(self):
        (_, err), _ = fetch(FakeResponse(404)); self.assertIn("not found", err)

    def test4_empty_input(self):
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=["", "   ", " Paris "]), contextlib.redirect_stdout(out):
            self.assertEqual(wa.get_city_input(), "Paris")
        self.assertEqual(out.getvalue().count("cannot be empty"), 2)

    def test5_invalid_key(self):
        (_, err), _ = fetch(FakeResponse(401)); self.assertIn("invalid or unauthorized", err)

    def test6_missing_key(self):
        out = io.StringIO()
        env = {k: v for k, v in os.environ.items() if k != "OPENWEATHER_API_KEY"}
        with mock.patch.dict(os.environ, env, clear=True), contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit): wa.get_api_key()
        self.assertIn("setx OPENWEATHER_API_KEY", out.getvalue())

    def test7_no_internet(self):
        (_, err), _ = fetch(side_effect=requests.exceptions.ConnectionError("x")); self.assertIn("internet", err)

    def test8_timeout(self):
        (_, err), _ = fetch(side_effect=requests.exceptions.Timeout("x")); self.assertIn("timed out", err)

    def test9_rate_limit(self):
        (_, err), _ = fetch(FakeResponse(429)); self.assertIn("rate limit", err)

    def test10_multiple_cities(self):
        out = run_main(["London", "Nowhere", "q"], [FakeResponse(200, GOOD), FakeResponse(404)])
        self.assertIn("Weather in London, GB", out); self.assertIn("not found", out); self.assertIn("Goodbye", out)

    def test_invalid_responses(self):
        for resp in (FakeResponse(200, {"cod": 200}), FakeResponse(200, bad_json=True),
                     FakeResponse(200, {"name": "X", "main": {}, "weather": [], "wind": {}})):
            (data, err), _ = fetch(resp); self.assertIsNone(data); self.assertIsNotNone(err)

    def test_server_error_and_unexpected(self):
        (_, err), _ = fetch(FakeResponse(500)); self.assertIn("500", err)
        (_, err), _ = fetch(side_effect=requests.exceptions.RequestException("x")); self.assertIn("failed", err)

    def test_conversion_and_display(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out): wa.display_weather(GOOD)
        t = out.getvalue()
        self.assertIn("20.0 °C / 68.0 °F", t); self.assertIn("Light Rain", t)
        self.assertIn("60%", t); self.assertIn("3.5 m/s", t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
