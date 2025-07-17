import logging

from src.schemas.sch_member import Member

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_member_repo_all(member_repo):
    members = member_repo.all()
    logger.info(f"Fetched {len(members)} members")
    assert isinstance(members, list)
    for m in members:
        logger.debug(f"Checking member: {m.memberid}")
        assert isinstance(m, Member)


def test_member_repo_get_by_ip(member_repo):
    members = member_repo.all()
    logger.info(f"Fetched {len(members)} members for IP test")
    if members:
        ip = members[0].ip
        logger.info(f"Testing get_by_ip with IP: {ip}")
        member = member_repo.get_by_ip(ip)
        logger.info(f"Result member: {member}")
        assert member is not None
        assert member.ip == ip
    else:
        logger.info("No members found, testing with dummy IP")
        assert member_repo.get_by_ip("127.0.0.1") is None


def test_member_repo_get_by_id(member_repo):
    members = member_repo.all()
    logger.info(f"Fetched {len(members)} members for ID test")
    if members:
        memberid = members[0].memberid
        logger.info(f"Testing get_by_id with memberid: {memberid}")
        member = member_repo.get_by_id(memberid)
        logger.info(f"Result member: {member}")
        assert member is not None
        assert member.memberid == memberid
    else:
        logger.info("No members found, testing with dummy ID")
        assert member_repo.get_by_id("dummyid") is None
