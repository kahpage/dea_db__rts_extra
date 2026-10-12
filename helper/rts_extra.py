# Note:
#  - as of today (2026.10.12), all RTS subgroups are included: https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E7%A7%8B%E5%AD%A3%E4%BE%8B%E5%A4%A7%E7%A5%AD
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    disabled_events: list[int | str] = []

    thwikicc = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E7%A7%8B%E5%AD%A3%E4%BE%8B%E5%A4%A7%E7%A5%AD"

    i = "sp1"  # ==== rts_sp1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_sp1 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%ADSP/%E7%AC%AC1%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "sp_reitaisaisp_bnr.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20110108031108/http://www.reitaisai.jp/img/reitaisaisp_bnr.jpg",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "sp_sp.JPG",
                [
                    Source(
                        "https://web.archive.org/web/20110226113125/http://reitaisai.jp/img/sp.JPG",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.6284445, 139.7926734),
                address="3 Chome-11-1 Ariake, Koto City, Tokyo 135-0063, Japan",
                description="東京ビッグサイト 東4・5・6ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20101008040306/http://www.reitaisai.jp/outline.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmniRNV84lzB1SNXuy60c0lznxgbqmNtYyJ8rkHQXk9u4qwSBeDafMEeWY7SaHOPcgw9m9BObYv4SvxJATFOtwEErABiE-oZjeBkl96ni8hTFClnpIJNnLLpRCBg6Ue9K__BWAAVQ=s0?imgmax=0",
                url="https://maps.app.goo.gl/6EYu64eY7PRhWRxu7",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭SP",
                "博麗神社例大祭SP",
                "Hakurei Jinja Reitaisai SP",
                "Reitaisai SP",
                "RTS SP",
                "博麗神社例大祭 (スペシャル)",
                "Hakurei Jinja Reitaisai Special",
                "RTS SP1",
            ],
            dates="2010.09.19",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20101008040306/http://www.reitaisai.jp/outline.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20100703080700/http://reitaisai.jp/result.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_sp1} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.06",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "sp2"  # ==== rts_sp2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_sp2 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%ADSP/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.6284445, 139.7926734),
                address="3 Chome-11-1 Ariake, Koto City, Tokyo 135-0063, Japan",
                description="東京ビッグサイト",
                sources=[
                    Source(
                        "https://web.archive.org/web/20111109155922mp_/http://www.reitaisai.jp/outline.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmniRNV84lzB1SNXuy60c0lznxgbqmNtYyJ8rkHQXk9u4qwSBeDafMEeWY7SaHOPcgw9m9BObYv4SvxJATFOtwEErABiE-oZjeBkl96ni8hTFClnpIJNnLLpRCBg6Ue9K__BWAAVQ=s0?imgmax=0",
                url="https://maps.app.goo.gl/6EYu64eY7PRhWRxu7",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭SP2",
                "博麗神社例大祭SP2",
                "Hakurei Jinja Reitaisai SP2",
                "Reitaisai SP2",
                "RTS SP2",
                "博麗神社例大祭 (スペシャル2)",
                "Hakurei Jinja Reitaisai Special 2",
            ],
            dates="2011.09.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20111109155922mp_/http://www.reitaisai.jp/outline.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20111123184511/http://reitaisai.jp/circlelists/search/circles/0",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_sp2} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw1"  # ==== rts_tw1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw1 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC1%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw1_rtstw1.jpg",
                [Source(thwikicc_tw1, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            Medium(
                "tw1_RTSTW_map-265x300.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20150526041319/http://reitaisai.com/rtstw/circle-list",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0617771, 121.4914951),
                address="No. 2, Section 1, New Taipei Blvd, Zhongshan Village, Sanchong District, New Taipei City, Taiwan 241",
                description="三重区綜合体育館",
                sources=[
                    Source(
                        "https://web.archive.org/web/20150625154819/http://reitaisai.com/rtstw/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9SUhEIH7yhJ6MMhvx8gglEc-Y_3jnsCdrh61JHSozlObZgQ6ChpBjoiedKKKfGpRG0utO5y1-YcZZmv5Kic8f8_JNEGpjqIwkO8PR6GIMQpnM7T5n4-78jiWOWmprtJ0QiMFGlg=s0?imgmax=0",
                url="https://maps.app.goo.gl/jhWDgcEd63Se7M3V6",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣1",
                "博麗神社例大祭in台灣1",
                "Hakurei Jinja Reitaisai in Taiwan 1",
                "Reitaisai in Taiwan 1",
                "RTS TW1",
                "第一回博麗神社例大祭in台灣",
            ],
            dates="2015.06.06",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20150625154819/http://reitaisai.com/rtstw/",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20150526041319/http://reitaisai.com/rtstw/circle-list",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_tw1} (not sourced)",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw1.5"  # ==== rts_tw1.5 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw1_5 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE%231_5"

        media_ = [
            Medium(
                "1.5_rts1.5.jpg",
                [
                    Source(
                        thwikicc_tw1_5, (ReliabilityTypes.Likely, OriginTypes.External)
                    )
                ],
            ),
            Medium(
                "tw1.5_CU4waLrUAAA9tTi.jpg",
                [
                    Source(
                        "https://x.com/HakureijinjyaS/status/670526622018232320",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0216697, 121.5352956),
                address="No. 1號, Section 4, Roosevelt Rd, Xuefu Village, Da’an District, Taipei City, Taiwan 106",
                description="台湾大学綜合体育館１階",
                sources=[
                    Source(
                        "https://live.nicovideo.jp/watch/lv252981576",
                        (ReliabilityTypes.Reliable, OriginTypes.OfficialExt),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9TgQ77cRam5Gc-B66TLwY_1lp5cvWrkZXd9sTteRFItUFA7Oip4oOU4n38sxDYiRIG0jFGPDAtXTaorMrQ7Hte97lcHIOw9zu_jMM3M8VP4ZBmIfn5KCQNP5omab40ei_Qk529j=s0?imgmax=0",
                url="https://maps.app.goo.gl/a9rCjTYbVyUtwxMB9",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣1.5",
                "博麗神社例大祭in台灣1.5",
                "Hakurei Jinja Reitaisai in Taiwan 1.5",
                "Reitaisai in Taiwan 1.5",
                "RTS TW1.5",
                "東方Project～petit only～with博麗神社例大祭",
                "Touhou Project ~petit only~ with Hakurei Jinja Reitaisai",
            ],
            dates="2016.02.21",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://live.nicovideo.jp/watch/lv252981576",
                    (ReliabilityTypes.Reliable, OriginTypes.OfficialExt),
                ),
                Source(
                    "Other source, TW1.5 alias: https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE%231_5",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
                Source(
                    "Main URL (dead) referenced here: https://x.com/HakureijinjyaS/status/700969067671195649",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
                Source(
                    "Participating circles (day 1): https://web.archive.org/web/20160408114127/http://gjs.tw/ch/group_list.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (day 2): https://web.archive.org/web/20160226150433/http://gjs.tw/ch/group_list2.html",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    'Is also "東方Project～petit only～with博麗神社例大祭": https://x.com/HakureijinjyaS/status/666863172494557184',
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "About ~petit only~: https://web.archive.org/web/20160913174534/http://reitaisai.com/rts13/petit-only-with-reitaisai",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Misc source for ~petit only~: https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E4%B8%9C%E6%96%B9Project%EF%BD%9Epetit_only%EF%BD%9Ewith%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD%231",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description="Part of the 2016 edition of Comic Horizon.",
            comments='I could not find any evidence of the "TW1.5" alias, but it probably still should be included in the RTS database.\n~petit only~ 2 is also hk1 (see the respective page for more info)',
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw2"  # ==== rts_tw2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw2 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw2_rtstw2.jpg",
                [
                    Source(
                        thwikicc_tw2, (ReliabilityTypes.Reliable, OriginTypes.Official)
                    )
                ],
            ),
            Medium(
                "tw2_2bc525_3b1e389cb0604fc88e410e4c096ddcdc~mv2_d_2738_1208_s_2.avif",
                [
                    Source(
                        "https://afongcp.wixsite.com/rtstw2/clist",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw2_2bc525_54007ee9b2d942c3971066bd90a1ca87~mv2_d_2185_1575_s_2.avif",
                [
                    Source(
                        "https://afongcp.wixsite.com/rtstw2", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0725177, 121.5182936),
                address="No. 232, Section 3, Chengde Rd, Bao'an Village, Datong District, Taipei City, Taiwan 103",
                description="台灣台北市大同區承德路三段232號B1,B2(橡木桶洋酒旁)",
                sources=[
                    Source(
                        "https://afongcp.wixsite.com/rtstw2/map",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=29YYFfX8ISuW4-rg6412eA&cb_client=search.gws-prod.gps&w=612&h=360&yaw=283.37595&pitch=-30&thumbfov=100",
                url="https://maps.app.goo.gl/gqKSczgxDXZtZMPLA",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣2",
                "博麗神社例大祭in台灣2",
                "Hakurei Jinja Reitaisai in Taiwan 2",
                "Reitaisai in Taiwan 2",
                "RTS TW2",
                "第二回博麗神社例大祭in台灣",
            ],
            dates="2017.05.28",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://afongcp.wixsite.com/rtstw2/about",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://afongcp.wixsite.com/rtstw2/clist",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_tw2} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.08",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw3"  # ==== rts_tw3 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw3 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC3%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw3_rtstw3.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw3_37f26f8d8d288a31e45869bdde549f8e.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20260921220653/https://reitaisai.com/tw3/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw3_22ec47cadb7bfe7584116ab265fb9c4e-860x860-860x860.gif",
                [
                    Source(
                        "https://web.archive.org/web/20260512005348/https://reitaisai.com/tw3/2019/02/27/circle-list/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw3_RZZHxrk.jpeg",
                [
                    Source(
                        "https://afongcp.wixsite.com/rtstw3/c-list",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0438366, 121.5593508),
                address="No. 133號, Guangfu S Rd, Xinren Village, Xinyi District, Taipei City, Taiwan 11072",
                description="松山文創園區 多功能展演廳",
                sources=[
                    Source(
                        "https://web.archive.org/web/20260512005348/https://reitaisai.com/tw3/2019/01/15/%e9%96%8b%e5%82%ac%e6%83%85%e5%a0%b1/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9QKzYJ37a3BAnwW18RdxdpZJBWG4daRphf5woZQxOFrgjc9ID_UVYsrjLK6_2p0FTTnEouI2CnpclvuCLzOKBwvk7zDm7KsgihbYu6DGCbfJ1vmc77wA8B_b011ZL_w0gOYGioUDw=w408-h272-k-no",
                url="https://maps.app.goo.gl/xcfMdQeHCT1PaSN9A",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣3",
                "博麗神社例大祭in台灣3",
                "Hakurei Jinja Reitaisai in Taiwan 3",
                "Reitaisai in Taiwan 3",
                "RTS TW3",
                "第三回博麗神社例大祭in台灣",
            ],
            dates="2019.06.16",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20260512005348/https://reitaisai.com/tw3/2019/01/15/%e9%96%8b%e5%82%ac%e6%83%85%e5%a0%b1/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20260512005348/https://reitaisai.com/tw3/2019/02/27/circle-list/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (2): https://afongcp.wixsite.com/rtstw3/c-list",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles (3): {thwikicc_tw3}",
                    (RT.Likely, OT.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw4"  # ==== rts_tw4 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw4 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC4%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw4_20243SP.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw4_RTStw4_jp.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw4_20243OUT.png",
                [
                    Source(
                        "https://web.archive.org/web/20260921220653/https://reitaisai.com/tw4-zh-tw/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw4_efb55a4f74ff5c79fdb3777215db8f6d.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20260512005310/https://reitaisai.com/tw4/acceptance_circle/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0617771, 121.4914951),
                address="No. 2, Section 1, New Taipei Blvd, Zhongshan Village, Sanchong District, New Taipei City, 台湾 241",
                description="新北市三重區綜合體育館",
                sources=[
                    Source(
                        "https://web.archive.org/web/20260921220653/https://reitaisai.com/tw4-zh-tw/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9TmNIuF3orCB2pd7TND3WGUUaw90C_UhUbfpwZJNDJb6syZaoOCPIFzjcARDA-oEYm90nx-W1DhUtL7fn5LuWZMtvWiyl9VkmyH2TUaRlH-fdhzFJR5ZqElu5328B-FBVRPM_Sf=s0?imgmax=0",
                url="https://maps.app.goo.gl/9A5hPxncfZqQJyx57",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣4",
                "博麗神社例大祭in台灣4",
                "Hakurei Jinja Reitaisai in Taiwan 4",
                "Reitaisai in Taiwan 4",
                "RTS TW4",
                "第四回博麗神社例大祭in台灣",
            ],
            dates="2024.09.14",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20260921220653/https://reitaisai.com/tw4-zh-tw/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20260512005310/https://reitaisai.com/tw4/acceptance_circle/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (2): https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC4%E5%B1%8A%E6%91%8A%E4%BD%8D",
                    (RT.Likely, OT.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "tw5"  # ==== rts_tw5 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_tw5 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E5%8F%B0%E6%B9%BE/%E7%AC%AC5%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "tw5_tw5-zh-tw.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw5_tw5-ja.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "tw5_pc-1.png",
                [
                    Source(
                        "https://web.archive.org/web/20260620153530/https://reitaisai.com/tw5/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(25.0438366, 121.5606383),
                address="No. 133號, Guangfu S Rd, Xinren Village, Xinyi District, Taipei City, 台湾 11072",
                description="松山文創園区 / 松山文創園區",
                sources=[
                    Source(
                        "https://web.archive.org/web/20260921220654/https://reitaisai.com/tw5-zh-tw/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9QKzYJ37a3BAnwW18RdxdpZJBWG4daRphf5woZQxOFrgjc9ID_UVYsrjLK6_2p0FTTnEouI2CnpclvuCLzOKBwvk7zDm7KsgihbYu6DGCbfJ1vmc77wA8B_b011ZL_w0gOYGioUDw=s0?imgmax=0",
                url="https://maps.app.goo.gl/ysMAgRsqKEGHSoiM8",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in台灣5",
                "博麗神社例大祭in台灣5",
                "Hakurei Jinja Reitaisai in Taiwan 5",
                "Reitaisai in Taiwan 5",
                "RTS TW5",
                "第五回博麗神社例大祭in台灣",
            ],
            dates="2026.06.20",
            circles=[],
            media=media_,
            sources=[
                Source("Date: ", (RT.Reliable, OT.Official)),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20260620153542/https://reitaisai.com/tw5/circle-place-assign/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_tw5}",
                    (RT.Likely, OT.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "gt1"  # ==== rts_gt1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_gt1 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E6%96%B0%E6%BD%9F/%E7%AC%AC1%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "gt1_rtsgt1.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "gt1_b2788fa08b751b33185ba65359f5bbc1.png",
                [
                    Source(
                        "https://web.archive.org/web/20260512005257/https://reitaisai.com/gt/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(37.878947, 139.04623),
                address="〒950-1141 新潟県新潟市中央区鐘木１８５−１０",
                description="新潟市産業振興センター",
                sources=[
                    Source(
                        "https://web.archive.org/web/20260512005257/https://reitaisai.com/gt/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9TxbTscpEbhRmeoWW75jZqb-kPC5mYG93ZevrWt4jOFg3eRZwANloIyQ82lVPBpK6MN_eG5DawYa5ffm2rfUmEDqgZqRbJ2hmRDMGSeJ17zLZhjBcJb2rw50TFQNkzdkeYIIxQB=s0?imgmax=0",
                url="https://maps.app.goo.gl/BJ3pA99sF7BxLcCq6",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in新潟1",
                "博麗神社例大祭in新潟1",
                "Hakurei Jinja Reitaisai in Niigata 1",
                "Reitaisai in Niigata 1",
                "RTS GT1",
                "第一回博麗神社例大祭in新潟",
            ],
            dates="2022.03.20",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20260512005257/https://reitaisai.com/gt/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20260414152138/https://gataket.com/list/reitai_03c/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_gt1} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "gt2"  # ==== rts_gt2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_gt2 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E6%96%B0%E6%BD%9F/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "gt2_rtsgt2.png", [Source(thwikicc_gt2, (RT.Reliable, OT.Official))]
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(37.878947, 139.04623),
                address="〒950-1141 新潟県新潟市中央区鐘木１８５−１０",
                description="新潟市産業振興センター",
                sources=[
                    Source(
                        "https://web.archive.org/web/20241108085727/https://gataket.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9TxbTscpEbhRmeoWW75jZqb-kPC5mYG93ZevrWt4jOFg3eRZwANloIyQ82lVPBpK6MN_eG5DawYa5ffm2rfUmEDqgZqRbJ2hmRDMGSeJ17zLZhjBcJb2rw50TFQNkzdkeYIIxQB=s0?imgmax=0",
                url="https://maps.app.goo.gl/BJ3pA99sF7BxLcCq6",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in新潟2",
                "博麗神社例大祭in新潟2",
                "Hakurei Jinja Reitaisai in Niigata 2",
                "Reitaisai in Niigata 2",
                "RTS GT2",
                "第二回博麗神社例大祭in新潟",
                "博麗神社例大祭出張版inガタケット179",
                "Hakurei Jinja Reitaisai in Getaket 179",
            ],
            dates="2024.12.01",
            circles=[],
            media=media_,
            sources=[
                Source(
                    'Date, alias "博麗神社例大祭出張版inガタケット179", Participating circles (1): https://web.archive.org/web/20260514033013/https://gataket.com/list/g179/',
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_gt2} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description="Part of ガタケット179.",
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "gt3"  # ==== rts_gt3 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_gt3 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E6%96%B0%E6%BD%9F/%E7%AC%AC3%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "gt3_rtsgt3.png",
                [
                    Source(
                        thwikicc_gt3, (ReliabilityTypes.Reliable, OriginTypes.Official)
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(37.878947, 139.04623),
                address="〒950-1141 新潟県新潟市中央区鐘木１８５−１０",
                description="新潟市産業振興センター",
                sources=[
                    Source(
                        "https://web.archive.org/web/20250801053753/https://gataket.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9TxbTscpEbhRmeoWW75jZqb-kPC5mYG93ZevrWt4jOFg3eRZwANloIyQ82lVPBpK6MN_eG5DawYa5ffm2rfUmEDqgZqRbJ2hmRDMGSeJ17zLZhjBcJb2rw50TFQNkzdkeYIIxQB=s0?imgmax=0",
                url="https://maps.app.goo.gl/BJ3pA99sF7BxLcCq6",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in新潟3",
                "博麗神社例大祭in新潟3",
                "Hakurei Jinja Reitaisai in Niigata 3",
                "Reitaisai in Niigata 3",
                "RTS GT3",
                "第三回博麗神社例大祭in新潟",
                "博麗神社例大祭出張版inガタケット182",
                "Hakurei Jinja Reitaisai in Getaket 182",
            ],
            dates="2025.11.30",
            circles=[],
            media=media_,
            sources=[
                Source(
                    'Date, alias "博麗神社例大祭出張版inガタケット182", Participating circles (1): https://web.archive.org/web/20260609062104/https://gataket.com/list/g182/',
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_gt3} (well sourced)",
                    (ReliabilityTypes.Reliable, OriginTypes.External),
                ),
            ],
            locations=locations,
            description="Part of ガタケット182.",
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "s1"  # ==== rts_s1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            # Location(
            #     coordinates=(,),
            #     address="",
            #     description="",
            #     sources=[Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))],
            #     # comments=None,
            #     imageUrl="",
            #     url="",
            # ),
        ]
        event = Event(
            aliases=[
                "例大祭in静岡1",
                "博麗神社例大祭in静岡1",
                "Hakurei Jinja Reitaisai in Shizuoka 1",
                "Reitaisai in Shizuoka 1",
                "RTS S1",
                "第一回博麗神社例大祭in静岡",
            ],
            dates="unknown",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Should exist: as we know there is 例大祭in静岡2.",
                    (RT.Guess, OT.Unsourced),
                ),
                Source(
                    "Is RTS17: guess according to location and date.",
                    (RT.Guess, OT.Unsourced),
                ),
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
            ],
            locations=locations,
            description="Seems to be RTS17.",
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "s2"  # ==== rts_s2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_s2 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E9%9D%99%E5%86%88/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "s2_srts2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "s2_srts2_topImg_catalog.png",
                [
                    Source(
                        "https://web.archive.org/web/20260627025108/https://reitaisai.com/srts2/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "s2_534px-静冈例大祭2插画1.png",
                [
                    Source(
                        "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E9%9D%99%E5%86%88",
                        (RT.Likely, OT.External),
                    )
                ],
            ),
            Medium(
                "s2_924px-静冈例大祭2插画2.png",
                [
                    Source(
                        "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD_in_%E9%9D%99%E5%86%88",
                        (RT.Likely, OT.External),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.9713021, 138.403819),
                address="Japan, 〒422-8006 Shizuoka, Suruga Ward, Magarikane, 3 Chome−1−10 西館",
                description="ツインメッセ静岡",
                sources=[
                    Source(
                        "https://web.archive.org/web/20260627025108/https://reitaisai.com/srts2/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://maps.app.goo.gl/rMQ2csVhzjv39cpT9",
                url="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmxrusm9oXeDGfebZn1cc-XxrxsyXLw8CKmlHRwzlLJ9XVrCYPUjJR-bFYfj3cked2QbGmX4gOgAExEn2iuxaM0DdyeJsjf48AfEIH0pomBKS9L_r2HuwnT9dCzEXykzvJ1hsvpCkcojFg=s0?imgmax=0",
            ),
        ]
        event = Event(
            aliases=[
                "例大祭in静岡2",
                "博麗神社例大祭in静岡2",
                "Hakurei Jinja Reitaisai in Shizuoka 2",
                "Reitaisai in Shizuoka 2",
                "RTS S2",
                "SRTS2",
                "第二回博麗神社例大祭in静岡",
            ],
            dates="2025.03.23",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20260627025108/https://reitaisai.com/srts2/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20260512005317/https://reitaisai.com/srts2/circle-place-assign/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "yugeisai1"  # ==== rts_yugeisai1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_yugeisai1 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E6%B8%B8%E8%89%BA%E7%A5%AD%231"

        media_ = [
            Medium(
                "yugeisai1_afd625d7537899f3a1582ed2741b2489.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "yugeisai1_main_img.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20220102191955/http://yugeisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "yugeisai1_logo.svg",
                [
                    Source(
                        "https://web.archive.org/web/20220102191955/http://yugeisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.655153, 139.7607689),
                address="Japan, 〒105-7501 Tokyo, Minato City, Kaigan, 1 Chome−7−1 東京ポートシティ竹芝オフィスタワ",
                description="都立産業貿易センター 台東館7F",
                sources=[
                    Source(
                        "https://web.archive.org/web/20220102191955/http://yugeisai.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmihIGbPitN7h8Vc_sXo8I679FTgrlkYst2LWaAy_Wl45MDqMaFnozSO4Y2Vud8h07FgRpXdq_CPW3IWnFwj-AyKuJ0L7ShZyQ41TQcBAFNOouYZR3jFZXxn_SQsgsK-FST-5JK8g=w408-h544-k-no",
                url="https://maps.app.goo.gl/ZF8XaGQinUTwnNMw6",
            ),
        ]
        event = Event(
            aliases=[
                "遊芸祭1",
                "博麗神社遊芸祭1",
                "Hakurei Jinja Yugeisai 1",
                "第一回博麗神社遊芸祭",
            ],
            dates="2021.01.17 -> 2021.07.22",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date 1 (+ was cancelled): https://web.archive.org/web/20210123194857/http://yugeisai.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    'Date 2, "Yugeisai" in alias: https://web.archive.org/web/20210508005139/http://yugeisai.com/',
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Misc reference: {thwikicc_yugeisai1}", (RT.Likely, OT.External)
                ),
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.10",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "yugeisai2"  # ==== rts_yugeisai2 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_yugeisai2 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E6%B8%B8%E8%89%BA%E7%A5%AD%232"

        media_ = [
            Medium(
                "yugeisai2_54b16e368a7f1459ab4fe7b986fb2e29.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            Medium(
                "https://web.archive.org/web/20221204045429im_/https://yugeisai.com/wp-content/uploads/2022/05/%E9%81%8A%E8%8A%B8%E7%A5%AD%E5%8B%95%E7%94%BB%E7%94%A8v8-3.mp4",
                [
                    Source(
                        "https://web.archive.org/web/20221204045429im_/https://yugeisai.com/wp-content/uploads/2022/05/%E9%81%8A%E8%8A%B8%E7%A5%AD%E5%8B%95%E7%94%BB%E7%94%A8v8-3.mp4",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "yugeisai2_アセット-5@2x.png",
                [
                    Source(
                        "https://web.archive.org/web/20221204045429/https://yugeisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "yugeisai2_アセット-4@2x.png",
                [
                    Source(
                        "https://web.archive.org/web/20221204045429/https://yugeisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.655153, 139.7607689),
                address="Japan, 〒105-7501 Tokyo, Minato City, Kaigan, 1 Chome−7−1 東京ポートシティ竹芝オフィスタワ",
                comments=None,
                description="東京都立産業貿易センター 台東館 6階7階(受付:6階)",
                sources=[
                    Source(
                        "https://web.archive.org/web/20221204045909/https://yugeisai.com/summary/",
                        (ReliabilityTypes.Likely, OriginTypes.Official),
                    )
                ],
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmihIGbPitN7h8Vc_sXo8I679FTgrlkYst2LWaAy_Wl45MDqMaFnozSO4Y2Vud8h07FgRpXdq_CPW3IWnFwj-AyKuJ0L7ShZyQ41TQcBAFNOouYZR3jFZXxn_SQsgsK-FST-5JK8g=w408-h544-k-no",
                url="https://maps.app.goo.gl/ZF8XaGQinUTwnNMw6",
            ),
        ]
        event = Event(
            aliases=[
                "遊芸祭2",
                "博麗神社遊芸祭2",
                "Hakurei Jinja Yugeisai 2",
                "第二回博麗神社遊芸祭",
            ],
            dates="2022.07.18",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20221204045429/https://yugeisai.com/",
                    (RT.Reliable, OT.Official),
                ),
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
                Source(
                    f"Misc reference: {thwikicc_yugeisai2}", (RT.Likely, OT.External)
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.12",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "yugeisai3"  # ==== rts_yugeisai3 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_yugeisai3 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E6%B8%B8%E8%89%BA%E7%A5%AD%233"

        media_ = [
            Medium(
                "yugeisai3_0d638e399708caec9de87796c96a3079.png",
                [
                    Source(
                        "https://web.archive.org/web/20261008071823/https://reitaisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "yugeisai3_4F.png",
                [
                    Source(
                        "https://web.archive.org/web/20231128171902/https://yugeisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "yugeisai3_アセット-36-1.png",
                [
                    Source(
                        "https://web.archive.org/web/20231128171902/https://yugeisai.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.655153, 139.7607689),
                address="Japan, 〒105-7501 Tokyo, Minato City, Kaigan, 1 Chome−7−1 東京ポートシティ竹芝オフィスタワ",
                comments=None,
                description="東京都立産業貿易センター 浜松町館",
                sources=[
                    Source(
                        "https://web.archive.org/web/20231128171902/https://yugeisai.com/",
                        (ReliabilityTypes.Likely, OriginTypes.Official),
                    )
                ],
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWmihIGbPitN7h8Vc_sXo8I679FTgrlkYst2LWaAy_Wl45MDqMaFnozSO4Y2Vud8h07FgRpXdq_CPW3IWnFwj-AyKuJ0L7ShZyQ41TQcBAFNOouYZR3jFZXxn_SQsgsK-FST-5JK8g=w408-h544-k-no",
                url="https://maps.app.goo.gl/ZF8XaGQinUTwnNMw6",
            ),
        ]
        event = Event(
            aliases=[
                "遊芸祭3",
                "博麗神社遊芸祭3",
                "Hakurei Jinja Yugeisai 3",
                "第三回博麗神社遊芸祭",
            ],
            dates="2023.07.09",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20231128171902/https://yugeisai.com/",
                    (RT.Reliable, OT.Official),
                ),
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
                Source(
                    f"Misc reference: {thwikicc_yugeisai3}", (RT.Likely, OT.External)
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.12",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "ccb1"  # ==== rts_ccb1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_ccb1 = "https://thwiki.cc/%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD%E5%87%BA%E5%B7%AE%E7%89%88_in_%E7%A7%A9%E7%88%B6"

        media_ = [
            Medium(
                "ccb1_cover.png",
                [
                    Source(
                        "https://hamp.ai/event/rtschichibu",
                        (RT.Reliable, OT.OfficialExt),
                    )
                ],
            ),
            Medium(
                "ccb1_square.png",
                [
                    Source(
                        "https://hamp.ai/event/rtschichibu", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            Medium(
                "ccb1_map_with_circles.svg",
                [
                    Source(
                        "https://hamp.ai/event/rtschichibu", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.9986878, 139.0857789),
                address="Japan, 〒368-0046 Saitama, Chichibu, Miyakawacho, 1−7 秩父地場産センタ 3階",
                description="秩父市地場産業センター・秩父神社 参集殿",
                sources=[
                    Source(
                        "http://web.archive.org/web/20260921220654/https://reitaisai.com/ccb/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9SjChRjpt4udBWHh2MifWc5LyUOsTSCV3QLB6Q1O9dbvIdTa6H4yrrSAUNwHtCEpu8EoI3SKW4fNoHcpMAJEGqBeJ-gDf0p-PWMnrmLE-8gOmxiZq7VN-70zuXm79iEhv66tQM--P65krmZ=s0?imgmax=0",
                url="https://maps.app.goo.gl/DZ2icP49ysfpAeX96",
            ),
        ]
        event = Event(
            aliases=[
                "博麗神社例大祭出張版 in 秩父",
                "Hakurei Jinja Reitaisai Shuchouban in Chichibu",
            ],
            dates="2026.08.30",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: http://web.archive.org/web/20260921220654/https://reitaisai.com/ccb/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://hamp.ai/event/rtschichibu?subEvent=%E5%8D%9A%E9%BA%97%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD%E5%87%BA%E5%BC%B5%E7%89%88in%E7%A7%A9%E7%88%B6",
                    (RT.Reliable, OT.OfficialExt),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.12",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = "hk1"  # ==== rts_hk1 ====
    if i not in disabled_events:
        event_name = f"rts_{i}"
        print(f"Processing {event_name} ...")
        thwikicc_hk1 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E4%B8%9C%E6%96%B9Project%EF%BD%9Epetit_only%EF%BD%9Ewith%E5%8D%9A%E4%B8%BD%E7%A5%9E%E7%A4%BE%E4%BE%8B%E5%A4%A7%E7%A5%AD%23in%E9%A6%99%E6%B8%AF"

        media_ = [
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(22.2810524, 114.1705286),
                address="1號 Expo Dr, Wan Chai, Hong Kong Island, Hong Kong",
                description="香港會議展覽中心Hall3",
                sources=[
                    Source(
                        "https://web.archive.org/web/20170625055857/http://www.doujin-cp.com/zh/home-page-zh/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9Rd1uECzBro8V8y9Xt8xWisApIqE72gxTbp8fiMOKfb5kIkxSHKfDkvU_uA0sa1AZc-V-GGwYQp32qk3XPOMg9YBSia3HDNbsnvbNRflMSlUiq4bkcTuPAjo5wrqGehBNiVJpUdAU53Fao=s0?imgmax=0",
                url="https://maps.app.goo.gl/ndcewRJ9RUHrmriw8",
            ),
        ]
        event = Event(
            aliases=[
                "東方Project～petit only～with博麗神社例大祭in香港",
                "Touhou Project ~petit only~ with Hakurei Jinja Reitaisai in Hong Kong",
            ],
            dates="2017.07.28 - 2017.07.29 → CANCELLED",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://x.com/HakureijinjyaS/status/849897663956869120",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Was cancelled: https://x.com/HakureijinjyaS/status/866129451821654017",
                    (RT.Reliable, OT.Official),
                ),
                Source(f"Misc reference: {thwikicc_hk1}", (RT.Likely, OT.External)),
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
            ],
            locations=locations,
            description="Part of Creative Paradise 04.",
            comments="~petit only~ 1 is also tw1.5 (see the respective page for more info)",
            last_edited="2026.10.10",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    # i =   # ==== rts_ ====
    # if i not in disabled_events:
    #     event_name = f"rts_{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     coordinates=(,),
    #         #     address="",
    #         #     description="",
    #         #     sources=[Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))],
    #         #     # comments=None,
    #         #     imageUrl="",
    #         #     url="",
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=,
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             # Source("Date: ", (RT.Reliable, OT.Official)),
    #             # Source("Participating circles: ", (RT.Reliable, OT.Official)),
    #         ],
    #         locations=locations,
    #         description=None,
    #         # comments=None,
    #         last_edited="2026.10.10",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # ==== event group ====
    media = [
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = [
        "https://reitaisai.com/",
        "https://x.com/HakureijinjyaS",
        "https://www.youtube.com/channel/UCWgWAk02r-HKSYX2h6wnJVA",
        "https://x.com/reitaisai_sp",
        "https://x.com/yugeisai",
    ]

    event_group = EventGroup(
        aliases=[
            "博麗神社例大祭 (other events)",
            "Hakurei Jinja Reitaisai (other events)",
            "秋季例大祭 (other events)",
            "Reitaisai (other events)",
            "RTS (other events)",
        ],
        events=[],
        media=media,
        links=links,
        description="Collection of RTS (博麗神社例大祭) events not of the main numbered series, such as the SP (Special) events.",
        last_edited="2026.10.12",
        comments='Misc: "博麗電脳試遊会" is the name of the official committee of the gaming corner: https://x.com/shiyuu1443',
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
