#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pre-process the sample data and call node insertion methods."""
import os

from config import DATA_DIR
from graph_create.create_nodes import CreateNodesInGraph
from utils import decode_json
from graph_create.types import Severity


def create_nodes(*args, **kwargs):
    """Create nodes to the order of magnitude specified by kwargs.magnitude."""
    if len(args) > 0 or "mul_fact" in kwargs:
        if len(args) != 0:
            suffix = args[0]
        else:
            suffix = kwargs["mul_fact"]
        suffix = str(suffix)
        # First create the dependency node.
        f = open(os.path.join(DATA_DIR, "dependency.json"))
        dependency_node = decode_json(f.read())
        CreateNodesInGraph.create_dependency_node(
            dependency_name=dependency_node["dependency_name"] + "_" + suffix,
            dependency_path=dependency_node["dependency_path"] + "_" + suffix,
        )
        # Now create two versions for the node.
        f = open(os.path.join(DATA_DIR, "dependency_version.json"))
        dependency_version = decode_json(f.read())
        # Modify this if the number of versions of a dependency needs to be changed.
        for i in (0, 2):
            CreateNodesInGraph.create_dependency_version_node(
                version="{}_{}_{}".format(
                    dependency_version["version"], suffix, str(i)
                ),
                dep_name="{}_{}_{}".format(
                    dependency_version["dependency_name"], suffix, str(i)
                ),
            )
        # Create a security event node. This will be equal to the number of dependency nodes.
        f = open(os.path.join(DATA_DIR, "security_event.json"))
        security_event = decode_json(f.read())
        CreateNodesInGraph.create_security_event_node(
            event_id=security_event["event_id"],
            event_type=security_event["event_type"],
            body=security_event["body"],
            title=security_event["title"],
        )
        # Create a probable vulnerability node. This will be half of all security event nodes.
        if i % 2 == 0:
            CreateNodesInGraph.create_probable_vuln_node("PCVE-20XX-{}".format(str(i)))
        # Create an identified CVE node for every alternate probable CVE node. This means there'll
        # be half the number of identified CVE nodes as probale CVE nodes.
        if i % 4 == 0:
            f = open(os.path.join(DATA_DIR, "identified_cve.json"))
            identified_cve = decode_json(f.read())
            CreateNodesInGraph.create_reported_cve_node(
                cve_id=identified_cve["cve_id"],
                cvss=identified_cve["cvss"],
                severity=Severity(identified_cve["severity"].lower()),
            )