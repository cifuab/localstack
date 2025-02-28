# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from mypy_boto3_route53 import Route53Client

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class Route53RecordSetProperties(TypedDict):
    Name: Optional[str]
    Type: Optional[str]
    AliasTarget: Optional[AliasTarget]
    CidrRoutingConfig: Optional[CidrRoutingConfig]
    Comment: Optional[str]
    Failover: Optional[str]
    GeoLocation: Optional[GeoLocation]
    HealthCheckId: Optional[str]
    HostedZoneId: Optional[str]
    HostedZoneName: Optional[str]
    Id: Optional[str]
    MultiValueAnswer: Optional[bool]
    Region: Optional[str]
    ResourceRecords: Optional[list[str]]
    SetIdentifier: Optional[str]
    TTL: Optional[str]
    Weight: Optional[int]


class AliasTarget(TypedDict):
    DNSName: Optional[str]
    HostedZoneId: Optional[str]
    EvaluateTargetHealth: Optional[bool]


class CidrRoutingConfig(TypedDict):
    CollectionId: Optional[str]
    LocationName: Optional[str]


class GeoLocation(TypedDict):
    ContinentCode: Optional[str]
    CountryCode: Optional[str]
    SubdivisionCode: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class Route53RecordSetProvider(ResourceProvider[Route53RecordSetProperties]):
    TYPE = "AWS::Route53::RecordSet"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[Route53RecordSetProperties],
    ) -> ProgressEvent[Route53RecordSetProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - Type
          - Name

        Create-only properties:
          - /properties/HostedZoneName
          - /properties/Name
          - /properties/HostedZoneId

        Read-only properties:
          - /properties/Id
        """
        model = request.desired_state
        route53 = request.aws_client_factory.route53

        if not model.get("HostedZoneId"):
            # if only name was provided for hosted zone
            hosted_zone_name = model.get("HostedZoneName")
            hosted_zone_id = self.get_hosted_zone_id_from_name(hosted_zone_name, route53)
            model["HostedZoneId"] = hosted_zone_id

        attr_names = [
            "Name",
            "Type",
            "SetIdentifier",
            "Weight",
            "Region",
            "GeoLocation",
            "Failover",
            "MultiValueAnswer",
            "TTL",
            "ResourceRecords",
            "AliasTarget",
            "HealthCheckId",
        ]
        attrs = util.select_attributes(model, attr_names)

        if "AliasTarget" in attrs:
            # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-aliastarget.html
            if "EvaluateTargetHealth" not in attrs["AliasTarget"]:
                attrs["AliasTarget"]["EvaluateTargetHealth"] = False
        else:
            # TODO: CNAME & SOA only allow 1 record type. should we check that here?
            attrs["ResourceRecords"] = [{"Value": record} for record in attrs["ResourceRecords"]]

        if "TTL" in attrs:
            if isinstance(attrs["TTL"], str):
                attrs["TTL"] = int(attrs["TTL"])

        route53.change_resource_record_sets(
            HostedZoneId=model["HostedZoneId"],
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": attrs,
                    },
                ]
            },
        )
        # TODO: not 100% sure this behaves the same between alias and non-alias records
        model["Id"] = model["Name"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
        )

    def get_hosted_zone_id_from_name(self, hosted_zone_name: str, client: "Route53Client"):
        if not hosted_zone_name:
            raise Exception("Either HostedZoneId or HostedZoneName must be present.")

        zones = client.list_hosted_zones_by_name(DNSName=hosted_zone_name)["HostedZones"]
        if len(zones) != 1:
            raise Exception(f"Ambiguous HostedZoneName {hosted_zone_name} provided.")

        hosted_zone_id = zones[0]["Id"]
        return hosted_zone_id

    def read(
        self,
        request: ResourceRequest[Route53RecordSetProperties],
    ) -> ProgressEvent[Route53RecordSetProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[Route53RecordSetProperties],
    ) -> ProgressEvent[Route53RecordSetProperties]:
        """
        Delete a resource


        """
        model = request.previous_state
        route53 = request.aws_client_factory.route53
        rrset_kwargs = {
            "Name": model["Name"],
            "Type": model["Type"],
        }

        if "AliasTarget" in model:
            rrset_kwargs["AliasTarget"] = model["AliasTarget"]
        if "ResourceRecords" in model:
            rrset_kwargs["ResourceRecords"] = [
                {"Value": record} for record in model["ResourceRecords"]
            ]
        if "TTL" in model:
            rrset_kwargs["TTL"] = int(model["TTL"])

        route53.change_resource_record_sets(
            HostedZoneId=model["HostedZoneId"],
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "DELETE",
                        "ResourceRecordSet": rrset_kwargs,
                    },
                ]
            },
        )
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
        )

    def update(
        self,
        request: ResourceRequest[Route53RecordSetProperties],
    ) -> ProgressEvent[Route53RecordSetProperties]:
        """
        Update a resource


        """
        raise NotImplementedError
